from pprint import pprint
from typing import Type, TypeVar, cast

from google.protobuf.message import Message

import proto.packet_definitions_pb2 as packets

MESSAGE_REGISTRY: dict[str, Type[Message]] = {
    name: getattr(packets, name) for name in packets.DESCRIPTOR.message_types_by_name
}

# pprint(MESSAGE_REGISTRY)

T = TypeVar("T", bound=Message)


def get_message_instance(message_type: str, message_class: Type[T]) -> T | None:
    """
    Get a message instance with proper type hints for IDE auto-completion.

    Args:
        message_type: The name of the message type (e.g., "PacketMotionData")
        message_class: The class type for type checking (e.g., packets.PacketMotionData)

    Returns:
        An instance of the message class with proper typing, or None if not found
    """
    if message_type in MESSAGE_REGISTRY:
        return cast(message_class, MESSAGE_REGISTRY[message_type]())
    return None


# Usage: IDE will have auto-completion for message_instance
message_instance = get_message_instance("PacketMotionData", packets.PacketMotionData)

if message_instance:
    print("Creating instance")
    pprint(message_instance)
    print(type(message_instance))

    # Now IDE provides auto-completion
    print(f"Header: {message_instance.header}")
    print(f"Car motion data count: {len(message_instance.car_motion_data)}")
