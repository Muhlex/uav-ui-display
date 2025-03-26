from typing import NamedTuple


def clamp(value: float, min_value: float, max_value: float):
	return max(min_value, min(value, max_value))


def map_range(value: float, old_min: float, old_max: float, new_min: float, new_max: float):
	return new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min)


class Observable:
	_data = {}
	_subscribers = {}

	def subscribe(self, field: str, callback, immediate=False):
		if field not in self._subscribers:
			self._subscribers[field] = []
		if immediate:
			callback(getattr(self, field))
		self._subscribers[field].append(callback)

	def __setattr__(self, field: str, value):
		prev_value = getattr(self, field)
		super().__setattr__(field, value)

		if field.startswith("_") or prev_value == value:
			return
		if field in self._subscribers:
			for callback in self._subscribers[field]:
				callback(value)

	def __getattr__(self, field):
		return self._data[field]


def singleton(cls):
	instances = {}

	def get_instance(*args, **kwargs):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]

	return get_instance


class Insets(NamedTuple):
	top: int
	right: int
	bottom: int
	left: int
