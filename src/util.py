from typing import NamedTuple

from math import sqrt, pow


def map_range(value: float, in_min: float, in_max: float, out_min: float, out_max: float):
	return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)


def ease_in_cubic(value: float):
	return value * value * value


def ease_in_circ(value: float):
	return 1 - sqrt(1 - pow(value, 2))


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
