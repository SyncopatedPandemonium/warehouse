from __future__ import annotations
import itertools
import datetime
import collections
import functools
from classes import Employee, Item, Warehouse
from typing import Any, Iterable, TypeVar, Callable, Protocol, Dict, Union


def no_transformation(value, **_kwargs):
    return value


# Type hints to explain the interface of Loader better, ignore if confusing
# The type of objects that Loader will generate
TargetClass = TypeVar("TargetClass")
# Type of records which Loader will consume
Record = dict


# Used to build object of type TargetClass. Can be a class!
class TargetBuilder(Protocol):
    def __call__(self, **kwargs: dict) -> TargetClass:
        ...


# Used to transform specific properties from a Record (for example: parse date)
class ValueTransformation(Protocol):
    def __call__(
        self,
        value: Any,
        property: str,
        record: Record,
        target_class: TargetClass,
        load_record: Callable[[Record], TargetClass],
    ) -> Any:
        ...


# Used to post-process the results of the Loader. Any-thing goes!
class PostProcessor(Protocol):
    def __call__(self, records: Iterable[TargetClass]) -> Any:
        ...


class Loader:
    """Can load most reasonable iterables of dictionaries
    into object structures"""

    def __init__(
        self,
        strategies: Dict[str, ValueTransformation],
        target_builder: TargetBuilder,
        default_strategy: ValueTransformation = no_transformation,
        post_processor: PostProcessor = no_transformation,
    ):
        self.strategies = strategies
        self.default_strategy = default_strategy
        self.target_builder = target_builder
        self.post_processor = post_processor

    def load_records(
        self, records: Iterable[Record]
    ) -> Union[Iterable[TargetClass], Any]:
        return self.post_processor(self.load_record(record) for record in records)

    def load_record(self, record: Record) -> TargetClass:
        kwargs = {
            key: self._apply_strategy(self._select_strategy(key), key, value, record)
            for key, value in record.items()
        }
        return self.target_builder(**kwargs)

    def _select_strategy(self, property: str) -> ValueTransformation:
        return self.strategies.get(property, self.default_strategy)

    def _apply_strategy(
        self, strategy: ValueTransformation, property: str, value: Any, record: Record
    ) -> Any:
        return strategy(
            value,
            property=property,
            record=record,
            target_class=self.target_builder,
            load_record=self.load_record,
        )


T = TypeVar("T")


def tree_flattener(root: T, children_attr: str) -> Iterable[T]:
    """Will traverse any tree and flatten it to an iterable"""
    children = root.__getattribute__(children_attr)
    if callable(children_attr):
        children = children()  # in case children_attr is actually a method!
    return itertools.chain(
        [root],
        itertools.chain.from_iterable(
            tree_flattener(c, children_attr) for c in children
        ),
    )


def forest_flattener(roots: Iterable[T], children_attr: str) -> Iterable[T]:
    """Will traverse any forest and flatten to an iterable"""
    return itertools.chain.from_iterable(
        tree_flattener(root, children_attr) for root in roots
    )


class PersonnelLoader(Loader):
    """Used to load records into instances of Employee,
    return iterable of *all* employees"""

    def __init__(self):
        super().__init__(
            target_builder=Employee,  # we want an iterable of Employee
            strategies={
                "head_of": lambda l, load_record, *_args, **_kwargs: [
                    load_record(r) for r in l
                ]  # special handling for "head_of"
            },
            post_processor=lambda f:
            # we want all employees, not just the top-level ones
            forest_flattener(f, "head_of"),
        )


class WarehouseLoader(Loader):
    """Used to load records into instances of Warehouse
    containing instances of Item"""

    # NOTE: This is neccesary because Item is not helpful
    # (doesn't store warehouse)
    # WarehouseItem could have been a class
    # but I was feeling fancy
    WarehouseItem = collections.namedtuple("WarehouseItem", ["item", "warehouse"])

    def __init__(self):
        super().__init__(
            target_builder=self._build_warehouse_item,
            strategies={
                "date_of_stock": lambda d, *_args, **_kwargs:
                # parse date_of_stock to datetime
                datetime.datetime.fromisoformat(d)
            },
            # don't just return items, group by warehouse instead!
            post_processor=self._group_by_warehouse,
        )

    def _build_warehouse_item(self, **kwargs):
        return __class__.WarehouseItem(
            item=Item(**kwargs), warehouse=kwargs["warehouse"]
        )

    def _group_by_warehouse(self, warehouse_items):
        # NOTE: this is neccesary because Warehouse.add_item is not helpful
        def add_item(warehouse, i):
            """Adds the actual item to a warehouse instance
            and returns the warehouse"""
            warehouse.add_item(i.item)
            return warehouse

        def build_warehouse(id, items):
            """Given an id and iterable of decorated items
            it will return a Warehouse with actual items"""
            return functools.reduce(add_item, items, Warehouse(id))

        def sorted_groupby(items, key):
            """Because itertools.groupby doesn't work (as expected)
            if the data is not sorted!"""
            return itertools.groupby(sorted(items, key=key), key=key)

        groupped_items = sorted_groupby(warehouse_items, key=lambda i: i.warehouse)
        return (build_warehouse(id, items) for id, items in groupped_items)
