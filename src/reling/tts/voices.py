from __future__ import annotations
from enum import StrEnum
from random import shuffle
from typing import cast

from reling.db.enums import Gender

__all__ = [
    'Voice',
]


class Voice(StrEnum):
    ALLOY = 'alloy'
    ECHO = 'echo'
    FABLE = 'fable'
    ONYX = 'onyx'
    NOVA = 'nova'
    SHIMMER = 'shimmer'

    @property
    def gender(self) -> Gender:
        match self:
            case Voice.ALLOY:
                return Gender.NONBINARY
            case Voice.ECHO:
                return Gender.MALE
            case Voice.FABLE:
                return Gender.NONBINARY
            case Voice.ONYX:
                return Gender.MALE
            case Voice.NOVA:
                return Gender.FEMALE
            case Voice.SHIMMER:
                return Gender.FEMALE
            case _:
                raise ValueError(f'Unknown voice: {self}')

    @staticmethod
    def pick_voices(*positions: Gender | None) -> tuple[Voice, ...]:
        """
        Pick random non-repeating voices with the specified genders
        (`None` denoting no gender preference for the given position).

        :raises ValueError: If there are not enough voices to satisfy the requirements.
        """
        pools = cast(dict[Gender | None, list[Voice]], {None: []})

        for gender in Gender:
            gender_voices = cast(list[Voice], [voice for voice in Voice if cast(Voice, voice).gender == gender])

            required_count = positions.count(gender)
            if len(gender_voices) < required_count:
                raise ValueError(f'Not enough voices of {gender}')

            shuffle(gender_voices)
            pools[cast(Gender, gender)] = gender_voices[:required_count]
            pools[None].extend(gender_voices[required_count:])

        if len(pools[None]) < positions.count(None):
            raise ValueError('Not enough voices')

        shuffle(pools[None])
        return tuple(pools[position].pop() for position in positions)
