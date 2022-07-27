"""Defines project entities"""
from dataclasses import dataclass
from typing import List


@dataclass
class User:
    """User data representation"""
    name: str


@dataclass
class Message:
    """Message data representation"""
    user: User
    value: str


@dataclass
class Topic:
    """Topic of messages"""
    messages = List[Message]
