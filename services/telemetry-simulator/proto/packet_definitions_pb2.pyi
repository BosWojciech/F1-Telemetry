import enums_pb2 as _enums_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PacketSize(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PACKET_SIZE_UNSPECIFIED: _ClassVar[PacketSize]
    PACKET_MOTION_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_SESSION_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_LAP_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_EVENT_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_PARTICIPANTS_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_CAR_SETUP_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_CAR_TELEMETRY_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_CAR_STATUS_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_FINAL_CLASSIFICATION_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_LOBBY_INFO_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_CAR_DAMAGE_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_SESSION_HISTORY_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_TYRE_SETS_DATA_SIZE: _ClassVar[PacketSize]
    PACKET_MOTION_EX_DATA_SIZE: _ClassVar[PacketSize]
PACKET_SIZE_UNSPECIFIED: PacketSize
PACKET_MOTION_DATA_SIZE: PacketSize
PACKET_SESSION_DATA_SIZE: PacketSize
PACKET_LAP_DATA_SIZE: PacketSize
PACKET_EVENT_DATA_SIZE: PacketSize
PACKET_PARTICIPANTS_DATA_SIZE: PacketSize
PACKET_CAR_SETUP_DATA_SIZE: PacketSize
PACKET_CAR_TELEMETRY_DATA_SIZE: PacketSize
PACKET_CAR_STATUS_DATA_SIZE: PacketSize
PACKET_FINAL_CLASSIFICATION_DATA_SIZE: PacketSize
PACKET_LOBBY_INFO_DATA_SIZE: PacketSize
PACKET_CAR_DAMAGE_DATA_SIZE: PacketSize
PACKET_SESSION_HISTORY_DATA_SIZE: PacketSize
PACKET_TYRE_SETS_DATA_SIZE: PacketSize
PACKET_MOTION_EX_DATA_SIZE: PacketSize

class PacketHeader(_message.Message):
    __slots__ = ()
    PACKET_FORMAT_FIELD_NUMBER: _ClassVar[int]
    GAME_YEAR_FIELD_NUMBER: _ClassVar[int]
    GAME_MAJOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    GAME_MINOR_VERSION_FIELD_NUMBER: _ClassVar[int]
    PACKET_VERSION_FIELD_NUMBER: _ClassVar[int]
    PACKET_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_UID_FIELD_NUMBER: _ClassVar[int]
    SESSION_TIME_FIELD_NUMBER: _ClassVar[int]
    FRAME_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    OVERALL_FRAME_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PLAYER_CAR_INDEX_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_PLAYER_CAR_INDEX_FIELD_NUMBER: _ClassVar[int]
    packet_format: int
    game_year: int
    game_major_version: int
    game_minor_version: int
    packet_version: int
    packet_id: int
    session_uid: int
    session_time: float
    frame_identifier: int
    overall_frame_identifier: int
    player_car_index: int
    secondary_player_car_index: int
    def __init__(self, packet_format: _Optional[int] = ..., game_year: _Optional[int] = ..., game_major_version: _Optional[int] = ..., game_minor_version: _Optional[int] = ..., packet_version: _Optional[int] = ..., packet_id: _Optional[int] = ..., session_uid: _Optional[int] = ..., session_time: _Optional[float] = ..., frame_identifier: _Optional[int] = ..., overall_frame_identifier: _Optional[int] = ..., player_car_index: _Optional[int] = ..., secondary_player_car_index: _Optional[int] = ...) -> None: ...

class CarMotionData(_message.Message):
    __slots__ = ()
    WORLD_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    WORLD_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    WORLD_POSITION_Z_FIELD_NUMBER: _ClassVar[int]
    WORLD_VELOCITY_X_FIELD_NUMBER: _ClassVar[int]
    WORLD_VELOCITY_Y_FIELD_NUMBER: _ClassVar[int]
    WORLD_VELOCITY_Z_FIELD_NUMBER: _ClassVar[int]
    WORLD_FORWARD_DIR_X_FIELD_NUMBER: _ClassVar[int]
    WORLD_FORWARD_DIR_Y_FIELD_NUMBER: _ClassVar[int]
    WORLD_FORWARD_DIR_Z_FIELD_NUMBER: _ClassVar[int]
    WORLD_RIGHT_DIR_X_FIELD_NUMBER: _ClassVar[int]
    WORLD_RIGHT_DIR_Y_FIELD_NUMBER: _ClassVar[int]
    WORLD_RIGHT_DIR_Z_FIELD_NUMBER: _ClassVar[int]
    G_FORCE_LATERAL_FIELD_NUMBER: _ClassVar[int]
    G_FORCE_LONGITUDINAL_FIELD_NUMBER: _ClassVar[int]
    G_FORCE_VERTICAL_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    world_position_x: float
    world_position_y: float
    world_position_z: float
    world_velocity_x: float
    world_velocity_y: float
    world_velocity_z: float
    world_forward_dir_x: int
    world_forward_dir_y: int
    world_forward_dir_z: int
    world_right_dir_x: int
    world_right_dir_y: int
    world_right_dir_z: int
    g_force_lateral: float
    g_force_longitudinal: float
    g_force_vertical: float
    yaw: float
    pitch: float
    roll: float
    def __init__(self, world_position_x: _Optional[float] = ..., world_position_y: _Optional[float] = ..., world_position_z: _Optional[float] = ..., world_velocity_x: _Optional[float] = ..., world_velocity_y: _Optional[float] = ..., world_velocity_z: _Optional[float] = ..., world_forward_dir_x: _Optional[int] = ..., world_forward_dir_y: _Optional[int] = ..., world_forward_dir_z: _Optional[int] = ..., world_right_dir_x: _Optional[int] = ..., world_right_dir_y: _Optional[int] = ..., world_right_dir_z: _Optional[int] = ..., g_force_lateral: _Optional[float] = ..., g_force_longitudinal: _Optional[float] = ..., g_force_vertical: _Optional[float] = ..., yaw: _Optional[float] = ..., pitch: _Optional[float] = ..., roll: _Optional[float] = ...) -> None: ...

class PacketMotionData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAR_MOTION_DATA_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    car_motion_data: _containers.RepeatedCompositeFieldContainer[CarMotionData]
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., car_motion_data: _Optional[_Iterable[_Union[CarMotionData, _Mapping]]] = ...) -> None: ...

class MarshalZone(_message.Message):
    __slots__ = ()
    ZONE_START_FIELD_NUMBER: _ClassVar[int]
    ZONE_FLAG_FIELD_NUMBER: _ClassVar[int]
    zone_start: float
    zone_flag: int
    def __init__(self, zone_start: _Optional[float] = ..., zone_flag: _Optional[int] = ...) -> None: ...

class WeatherForecastSample(_message.Message):
    __slots__ = ()
    SESSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIME_OFFSET_FIELD_NUMBER: _ClassVar[int]
    WEATHER_FIELD_NUMBER: _ClassVar[int]
    TRACK_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TRACK_TEMPERATURE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    AIR_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    AIR_TEMPERATURE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    RAIN_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    session_type: int
    time_offset: int
    weather: int
    track_temperature: int
    track_temperature_change: int
    air_temperature: int
    air_temperature_change: int
    rain_percentage: int
    def __init__(self, session_type: _Optional[int] = ..., time_offset: _Optional[int] = ..., weather: _Optional[int] = ..., track_temperature: _Optional[int] = ..., track_temperature_change: _Optional[int] = ..., air_temperature: _Optional[int] = ..., air_temperature_change: _Optional[int] = ..., rain_percentage: _Optional[int] = ...) -> None: ...

class PacketSessionData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    WEATHER_FIELD_NUMBER: _ClassVar[int]
    TRACK_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    AIR_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_LAPS_FIELD_NUMBER: _ClassVar[int]
    TRACK_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SESSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    FORMULA_FIELD_NUMBER: _ClassVar[int]
    SESSION_TIME_LEFT_FIELD_NUMBER: _ClassVar[int]
    SESSION_DURATION_FIELD_NUMBER: _ClassVar[int]
    PIT_SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
    GAME_PAUSED_FIELD_NUMBER: _ClassVar[int]
    IS_SPECTATING_FIELD_NUMBER: _ClassVar[int]
    SPECTATOR_CAR_INDEX_FIELD_NUMBER: _ClassVar[int]
    SLI_PRO_NATIVE_SUPPORT_FIELD_NUMBER: _ClassVar[int]
    NUM_MARSHAL_ZONES_FIELD_NUMBER: _ClassVar[int]
    MARSHAL_ZONES_FIELD_NUMBER: _ClassVar[int]
    SAFETY_CAR_STATUS_FIELD_NUMBER: _ClassVar[int]
    NETWORK_GAME_FIELD_NUMBER: _ClassVar[int]
    NUM_WEATHER_FORECAST_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    WEATHER_FORECAST_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    FORECAST_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    AI_DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    SEASON_LINK_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    WEEKEND_LINK_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    SESSION_LINK_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PIT_STOP_WINDOW_IDEAL_LAP_FIELD_NUMBER: _ClassVar[int]
    PIT_STOP_WINDOW_LATEST_LAP_FIELD_NUMBER: _ClassVar[int]
    PIT_STOP_REJOIN_POSITION_FIELD_NUMBER: _ClassVar[int]
    STEERING_ASSIST_FIELD_NUMBER: _ClassVar[int]
    BRAKING_ASSIST_FIELD_NUMBER: _ClassVar[int]
    GEARBOX_ASSIST_FIELD_NUMBER: _ClassVar[int]
    PIT_ASSIST_FIELD_NUMBER: _ClassVar[int]
    PIT_RELEASE_ASSIST_FIELD_NUMBER: _ClassVar[int]
    ERS_ASSIST_FIELD_NUMBER: _ClassVar[int]
    DRS_ASSIST_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_RACING_LINE_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_RACING_LINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    RULE_SET_FIELD_NUMBER: _ClassVar[int]
    TIME_OF_DAY_FIELD_NUMBER: _ClassVar[int]
    SESSION_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SPEED_UNITS_LEAD_PLAYER_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_UNITS_LEAD_PLAYER_FIELD_NUMBER: _ClassVar[int]
    SPEED_UNITS_SECONDARY_PLAYER_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_UNITS_SECONDARY_PLAYER_FIELD_NUMBER: _ClassVar[int]
    NUM_SAFETY_CAR_PERIODS_FIELD_NUMBER: _ClassVar[int]
    NUM_VIRTUAL_SAFETY_CAR_PERIODS_FIELD_NUMBER: _ClassVar[int]
    NUM_RED_FLAG_PERIODS_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    weather: int
    track_temperature: int
    air_temperature: int
    total_laps: int
    track_length: int
    session_type: int
    track_id: int
    formula: int
    session_time_left: int
    session_duration: int
    pit_speed_limit: int
    game_paused: int
    is_spectating: int
    spectator_car_index: int
    sli_pro_native_support: int
    num_marshal_zones: int
    marshal_zones: _containers.RepeatedCompositeFieldContainer[MarshalZone]
    safety_car_status: int
    network_game: int
    num_weather_forecast_samples: int
    weather_forecast_samples: _containers.RepeatedCompositeFieldContainer[WeatherForecastSample]
    forecast_accuracy: int
    ai_difficulty: int
    season_link_identifier: int
    weekend_link_identifier: int
    session_link_identifier: int
    pit_stop_window_ideal_lap: int
    pit_stop_window_latest_lap: int
    pit_stop_rejoin_position: int
    steering_assist: int
    braking_assist: int
    gearbox_assist: int
    pit_assist: int
    pit_release_assist: int
    ers_assist: int
    drs_assist: int
    dynamic_racing_line: int
    dynamic_racing_line_type: int
    game_mode: int
    rule_set: int
    time_of_day: int
    session_length: int
    speed_units_lead_player: int
    temperature_units_lead_player: int
    speed_units_secondary_player: int
    temperature_units_secondary_player: int
    num_safety_car_periods: int
    num_virtual_safety_car_periods: int
    num_red_flag_periods: int
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., weather: _Optional[int] = ..., track_temperature: _Optional[int] = ..., air_temperature: _Optional[int] = ..., total_laps: _Optional[int] = ..., track_length: _Optional[int] = ..., session_type: _Optional[int] = ..., track_id: _Optional[int] = ..., formula: _Optional[int] = ..., session_time_left: _Optional[int] = ..., session_duration: _Optional[int] = ..., pit_speed_limit: _Optional[int] = ..., game_paused: _Optional[int] = ..., is_spectating: _Optional[int] = ..., spectator_car_index: _Optional[int] = ..., sli_pro_native_support: _Optional[int] = ..., num_marshal_zones: _Optional[int] = ..., marshal_zones: _Optional[_Iterable[_Union[MarshalZone, _Mapping]]] = ..., safety_car_status: _Optional[int] = ..., network_game: _Optional[int] = ..., num_weather_forecast_samples: _Optional[int] = ..., weather_forecast_samples: _Optional[_Iterable[_Union[WeatherForecastSample, _Mapping]]] = ..., forecast_accuracy: _Optional[int] = ..., ai_difficulty: _Optional[int] = ..., season_link_identifier: _Optional[int] = ..., weekend_link_identifier: _Optional[int] = ..., session_link_identifier: _Optional[int] = ..., pit_stop_window_ideal_lap: _Optional[int] = ..., pit_stop_window_latest_lap: _Optional[int] = ..., pit_stop_rejoin_position: _Optional[int] = ..., steering_assist: _Optional[int] = ..., braking_assist: _Optional[int] = ..., gearbox_assist: _Optional[int] = ..., pit_assist: _Optional[int] = ..., pit_release_assist: _Optional[int] = ..., ers_assist: _Optional[int] = ..., drs_assist: _Optional[int] = ..., dynamic_racing_line: _Optional[int] = ..., dynamic_racing_line_type: _Optional[int] = ..., game_mode: _Optional[int] = ..., rule_set: _Optional[int] = ..., time_of_day: _Optional[int] = ..., session_length: _Optional[int] = ..., speed_units_lead_player: _Optional[int] = ..., temperature_units_lead_player: _Optional[int] = ..., speed_units_secondary_player: _Optional[int] = ..., temperature_units_secondary_player: _Optional[int] = ..., num_safety_car_periods: _Optional[int] = ..., num_virtual_safety_car_periods: _Optional[int] = ..., num_red_flag_periods: _Optional[int] = ...) -> None: ...

class LapData(_message.Message):
    __slots__ = ()
    LAST_LAP_TIME_IN_MS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LAP_TIME_IN_MS_FIELD_NUMBER: _ClassVar[int]
    SECTOR1_TIME_IN_MS_FIELD_NUMBER: _ClassVar[int]
    SECTOR1_TIME_MINUTES_FIELD_NUMBER: _ClassVar[int]
    SECTOR2_TIME_IN_MS_FIELD_NUMBER: _ClassVar[int]
    SECTOR2_TIME_MINUTES_FIELD_NUMBER: _ClassVar[int]
    DELTA_TO_CAR_IN_FRONT_IN_MS_FIELD_NUMBER: _ClassVar[int]
    DELTA_TO_RACE_LEADER_IN_MS_FIELD_NUMBER: _ClassVar[int]
    LAP_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    SAFETY_CAR_DELTA_FIELD_NUMBER: _ClassVar[int]
    CAR_POSITION_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LAP_NUM_FIELD_NUMBER: _ClassVar[int]
    PIT_STATUS_FIELD_NUMBER: _ClassVar[int]
    NUM_PIT_STOPS_FIELD_NUMBER: _ClassVar[int]
    SECTOR_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LAP_INVALID_FIELD_NUMBER: _ClassVar[int]
    PENALTIES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_WARNINGS_FIELD_NUMBER: _ClassVar[int]
    CORNER_CUTTING_WARNINGS_FIELD_NUMBER: _ClassVar[int]
    NUM_UNSERVED_DRIVE_THROUGH_PENS_FIELD_NUMBER: _ClassVar[int]
    NUM_UNSERVED_STOP_GO_PENS_FIELD_NUMBER: _ClassVar[int]
    GRID_POSITION_FIELD_NUMBER: _ClassVar[int]
    DRIVER_STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_STATUS_FIELD_NUMBER: _ClassVar[int]
    PIT_LANE_TIMER_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    PIT_LANE_TIME_IN_LANE_IN_MS_FIELD_NUMBER: _ClassVar[int]
    PIT_STOP_TIMER_IN_MS_FIELD_NUMBER: _ClassVar[int]
    PIT_STOP_SHOULD_SERVE_PEN_FIELD_NUMBER: _ClassVar[int]
    last_lap_time_in_ms: int
    current_lap_time_in_ms: int
    sector1_time_in_ms: int
    sector1_time_minutes: int
    sector2_time_in_ms: int
    sector2_time_minutes: int
    delta_to_car_in_front_in_ms: int
    delta_to_race_leader_in_ms: int
    lap_distance: float
    total_distance: float
    safety_car_delta: float
    car_position: int
    current_lap_num: int
    pit_status: int
    num_pit_stops: int
    sector: int
    current_lap_invalid: int
    penalties: int
    total_warnings: int
    corner_cutting_warnings: int
    num_unserved_drive_through_pens: int
    num_unserved_stop_go_pens: int
    grid_position: int
    driver_status: int
    result_status: int
    pit_lane_timer_active: int
    pit_lane_time_in_lane_in_ms: int
    pit_stop_timer_in_ms: int
    pit_stop_should_serve_pen: int
    def __init__(self, last_lap_time_in_ms: _Optional[int] = ..., current_lap_time_in_ms: _Optional[int] = ..., sector1_time_in_ms: _Optional[int] = ..., sector1_time_minutes: _Optional[int] = ..., sector2_time_in_ms: _Optional[int] = ..., sector2_time_minutes: _Optional[int] = ..., delta_to_car_in_front_in_ms: _Optional[int] = ..., delta_to_race_leader_in_ms: _Optional[int] = ..., lap_distance: _Optional[float] = ..., total_distance: _Optional[float] = ..., safety_car_delta: _Optional[float] = ..., car_position: _Optional[int] = ..., current_lap_num: _Optional[int] = ..., pit_status: _Optional[int] = ..., num_pit_stops: _Optional[int] = ..., sector: _Optional[int] = ..., current_lap_invalid: _Optional[int] = ..., penalties: _Optional[int] = ..., total_warnings: _Optional[int] = ..., corner_cutting_warnings: _Optional[int] = ..., num_unserved_drive_through_pens: _Optional[int] = ..., num_unserved_stop_go_pens: _Optional[int] = ..., grid_position: _Optional[int] = ..., driver_status: _Optional[int] = ..., result_status: _Optional[int] = ..., pit_lane_timer_active: _Optional[int] = ..., pit_lane_time_in_lane_in_ms: _Optional[int] = ..., pit_stop_timer_in_ms: _Optional[int] = ..., pit_stop_should_serve_pen: _Optional[int] = ...) -> None: ...

class PacketLapData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LAP_DATA_FIELD_NUMBER: _ClassVar[int]
    TIME_TRIAL_PB_CAR_IDX_FIELD_NUMBER: _ClassVar[int]
    TIME_TRIAL_RIVAL_CAR_IDX_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    lap_data: _containers.RepeatedCompositeFieldContainer[LapData]
    time_trial_pb_car_idx: int
    time_trial_rival_car_idx: int
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., lap_data: _Optional[_Iterable[_Union[LapData, _Mapping]]] = ..., time_trial_pb_car_idx: _Optional[int] = ..., time_trial_rival_car_idx: _Optional[int] = ...) -> None: ...

class FastestLapData(_message.Message):
    __slots__ = ()
    VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    LAP_TIME_FIELD_NUMBER: _ClassVar[int]
    vehicle_idx: int
    lap_time: float
    def __init__(self, vehicle_idx: _Optional[int] = ..., lap_time: _Optional[float] = ...) -> None: ...

class RetirementData(_message.Message):
    __slots__ = ()
    VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    vehicle_idx: int
    def __init__(self, vehicle_idx: _Optional[int] = ...) -> None: ...

class TeamMateInPitsData(_message.Message):
    __slots__ = ()
    VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    vehicle_idx: int
    def __init__(self, vehicle_idx: _Optional[int] = ...) -> None: ...

class RaceWinnerData(_message.Message):
    __slots__ = ()
    VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    vehicle_idx: int
    def __init__(self, vehicle_idx: _Optional[int] = ...) -> None: ...

class PenaltyData(_message.Message):
    __slots__ = ()
    PENALTY_TYPE_FIELD_NUMBER: _ClassVar[int]
    INFRINGEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    OTHER_VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    LAP_NUM_FIELD_NUMBER: _ClassVar[int]
    PLACES_GAINED_FIELD_NUMBER: _ClassVar[int]
    penalty_type: int
    infringement_type: int
    vehicle_idx: int
    other_vehicle_idx: int
    time: int
    lap_num: int
    places_gained: int
    def __init__(self, penalty_type: _Optional[int] = ..., infringement_type: _Optional[int] = ..., vehicle_idx: _Optional[int] = ..., other_vehicle_idx: _Optional[int] = ..., time: _Optional[int] = ..., lap_num: _Optional[int] = ..., places_gained: _Optional[int] = ...) -> None: ...

class SpeedTrapData(_message.Message):
    __slots__ = ()
    VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    IS_OVERALL_FASTEST_IN_SESSION_FIELD_NUMBER: _ClassVar[int]
    IS_DRIVER_FASTEST_IN_SESSION_FIELD_NUMBER: _ClassVar[int]
    FASTEST_VEHICLE_IDX_IN_SESSION_FIELD_NUMBER: _ClassVar[int]
    FASTEST_SPEED_IN_SESSION_FIELD_NUMBER: _ClassVar[int]
    vehicle_idx: int
    speed: float
    is_overall_fastest_in_session: int
    is_driver_fastest_in_session: int
    fastest_vehicle_idx_in_session: int
    fastest_speed_in_session: float
    def __init__(self, vehicle_idx: _Optional[int] = ..., speed: _Optional[float] = ..., is_overall_fastest_in_session: _Optional[int] = ..., is_driver_fastest_in_session: _Optional[int] = ..., fastest_vehicle_idx_in_session: _Optional[int] = ..., fastest_speed_in_session: _Optional[float] = ...) -> None: ...

class StartLightsData(_message.Message):
    __slots__ = ()
    NUM_LIGHTS_FIELD_NUMBER: _ClassVar[int]
    num_lights: int
    def __init__(self, num_lights: _Optional[int] = ...) -> None: ...

class DriveThroughPenaltyServedData(_message.Message):
    __slots__ = ()
    VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    vehicle_idx: int
    def __init__(self, vehicle_idx: _Optional[int] = ...) -> None: ...

class StopGoPenaltyServedData(_message.Message):
    __slots__ = ()
    VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    vehicle_idx: int
    def __init__(self, vehicle_idx: _Optional[int] = ...) -> None: ...

class FlashbackData(_message.Message):
    __slots__ = ()
    FLASHBACK_FRAME_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    FLASHBACK_SESSION_TIME_FIELD_NUMBER: _ClassVar[int]
    flashback_frame_identifier: int
    flashback_session_time: float
    def __init__(self, flashback_frame_identifier: _Optional[int] = ..., flashback_session_time: _Optional[float] = ...) -> None: ...

class ButtonsData(_message.Message):
    __slots__ = ()
    BUTTON_STATUS_FIELD_NUMBER: _ClassVar[int]
    button_status: int
    def __init__(self, button_status: _Optional[int] = ...) -> None: ...

class OvertakeData(_message.Message):
    __slots__ = ()
    OVERTAKING_VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    BEING_OVERTAKEN_VEHICLE_IDX_FIELD_NUMBER: _ClassVar[int]
    overtaking_vehicle_idx: int
    being_overtaken_vehicle_idx: int
    def __init__(self, overtaking_vehicle_idx: _Optional[int] = ..., being_overtaken_vehicle_idx: _Optional[int] = ...) -> None: ...

class EventDataDetails(_message.Message):
    __slots__ = ()
    FASTEST_LAP_FIELD_NUMBER: _ClassVar[int]
    RETIREMENT_FIELD_NUMBER: _ClassVar[int]
    TEAM_MATE_IN_PITS_FIELD_NUMBER: _ClassVar[int]
    RACE_WINNER_FIELD_NUMBER: _ClassVar[int]
    PENALTY_FIELD_NUMBER: _ClassVar[int]
    SPEED_TRAP_FIELD_NUMBER: _ClassVar[int]
    START_LIGHTS_FIELD_NUMBER: _ClassVar[int]
    DRIVE_THROUGH_PENALTY_SERVED_FIELD_NUMBER: _ClassVar[int]
    STOP_GO_PENALTY_SERVED_FIELD_NUMBER: _ClassVar[int]
    FLASHBACK_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    OVERTAKE_FIELD_NUMBER: _ClassVar[int]
    fastest_lap: FastestLapData
    retirement: RetirementData
    team_mate_in_pits: TeamMateInPitsData
    race_winner: RaceWinnerData
    penalty: PenaltyData
    speed_trap: SpeedTrapData
    start_lights: StartLightsData
    drive_through_penalty_served: DriveThroughPenaltyServedData
    stop_go_penalty_served: StopGoPenaltyServedData
    flashback: FlashbackData
    buttons: ButtonsData
    overtake: OvertakeData
    def __init__(self, fastest_lap: _Optional[_Union[FastestLapData, _Mapping]] = ..., retirement: _Optional[_Union[RetirementData, _Mapping]] = ..., team_mate_in_pits: _Optional[_Union[TeamMateInPitsData, _Mapping]] = ..., race_winner: _Optional[_Union[RaceWinnerData, _Mapping]] = ..., penalty: _Optional[_Union[PenaltyData, _Mapping]] = ..., speed_trap: _Optional[_Union[SpeedTrapData, _Mapping]] = ..., start_lights: _Optional[_Union[StartLightsData, _Mapping]] = ..., drive_through_penalty_served: _Optional[_Union[DriveThroughPenaltyServedData, _Mapping]] = ..., stop_go_penalty_served: _Optional[_Union[StopGoPenaltyServedData, _Mapping]] = ..., flashback: _Optional[_Union[FlashbackData, _Mapping]] = ..., buttons: _Optional[_Union[ButtonsData, _Mapping]] = ..., overtake: _Optional[_Union[OvertakeData, _Mapping]] = ...) -> None: ...

class PacketEventData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EVENT_STRING_CODE_FIELD_NUMBER: _ClassVar[int]
    EVENT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    event_string_code: str
    event_details: EventDataDetails
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., event_string_code: _Optional[str] = ..., event_details: _Optional[_Union[EventDataDetails, _Mapping]] = ...) -> None: ...

class ParticipantData(_message.Message):
    __slots__ = ()
    AI_CONTROLLED_FIELD_NUMBER: _ClassVar[int]
    DRIVER_ID_FIELD_NUMBER: _ClassVar[int]
    NETWORK_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    MY_TEAM_FIELD_NUMBER: _ClassVar[int]
    RACE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    NATIONALITY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    YOUR_TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    SHOW_ONLINE_NAMES_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    ai_controlled: int
    driver_id: int
    network_id: int
    team_id: int
    my_team: int
    race_number: int
    nationality: int
    name: str
    your_telemetry: int
    show_online_names: int
    platform: int
    def __init__(self, ai_controlled: _Optional[int] = ..., driver_id: _Optional[int] = ..., network_id: _Optional[int] = ..., team_id: _Optional[int] = ..., my_team: _Optional[int] = ..., race_number: _Optional[int] = ..., nationality: _Optional[int] = ..., name: _Optional[str] = ..., your_telemetry: _Optional[int] = ..., show_online_names: _Optional[int] = ..., platform: _Optional[int] = ...) -> None: ...

class PacketParticipantsData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NUM_ACTIVE_CARS_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    num_active_cars: int
    participants: _containers.RepeatedCompositeFieldContainer[ParticipantData]
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., num_active_cars: _Optional[int] = ..., participants: _Optional[_Iterable[_Union[ParticipantData, _Mapping]]] = ...) -> None: ...

class CarSetupData(_message.Message):
    __slots__ = ()
    FRONT_WING_FIELD_NUMBER: _ClassVar[int]
    REAR_WING_FIELD_NUMBER: _ClassVar[int]
    ON_THROTTLE_FIELD_NUMBER: _ClassVar[int]
    OFF_THROTTLE_FIELD_NUMBER: _ClassVar[int]
    FRONT_CAMBER_FIELD_NUMBER: _ClassVar[int]
    REAR_CAMBER_FIELD_NUMBER: _ClassVar[int]
    FRONT_TOE_FIELD_NUMBER: _ClassVar[int]
    REAR_TOE_FIELD_NUMBER: _ClassVar[int]
    FRONT_SUSPENSION_FIELD_NUMBER: _ClassVar[int]
    REAR_SUSPENSION_FIELD_NUMBER: _ClassVar[int]
    FRONT_ANTI_ROLL_BAR_FIELD_NUMBER: _ClassVar[int]
    REAR_ANTI_ROLL_BAR_FIELD_NUMBER: _ClassVar[int]
    FRONT_SUSPENSION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    REAR_SUSPENSION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    BRAKE_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    BRAKE_BIAS_FIELD_NUMBER: _ClassVar[int]
    REAR_LEFT_TYRE_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    REAR_RIGHT_TYRE_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    FRONT_LEFT_TYRE_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    FRONT_RIGHT_TYRE_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    BALLAST_FIELD_NUMBER: _ClassVar[int]
    FUEL_LOAD_FIELD_NUMBER: _ClassVar[int]
    front_wing: int
    rear_wing: int
    on_throttle: int
    off_throttle: int
    front_camber: float
    rear_camber: float
    front_toe: float
    rear_toe: float
    front_suspension: int
    rear_suspension: int
    front_anti_roll_bar: int
    rear_anti_roll_bar: int
    front_suspension_height: int
    rear_suspension_height: int
    brake_pressure: int
    brake_bias: int
    rear_left_tyre_pressure: float
    rear_right_tyre_pressure: float
    front_left_tyre_pressure: float
    front_right_tyre_pressure: float
    ballast: int
    fuel_load: float
    def __init__(self, front_wing: _Optional[int] = ..., rear_wing: _Optional[int] = ..., on_throttle: _Optional[int] = ..., off_throttle: _Optional[int] = ..., front_camber: _Optional[float] = ..., rear_camber: _Optional[float] = ..., front_toe: _Optional[float] = ..., rear_toe: _Optional[float] = ..., front_suspension: _Optional[int] = ..., rear_suspension: _Optional[int] = ..., front_anti_roll_bar: _Optional[int] = ..., rear_anti_roll_bar: _Optional[int] = ..., front_suspension_height: _Optional[int] = ..., rear_suspension_height: _Optional[int] = ..., brake_pressure: _Optional[int] = ..., brake_bias: _Optional[int] = ..., rear_left_tyre_pressure: _Optional[float] = ..., rear_right_tyre_pressure: _Optional[float] = ..., front_left_tyre_pressure: _Optional[float] = ..., front_right_tyre_pressure: _Optional[float] = ..., ballast: _Optional[int] = ..., fuel_load: _Optional[float] = ...) -> None: ...

class PacketCarSetupData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAR_SETUPS_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    car_setups: _containers.RepeatedCompositeFieldContainer[CarSetupData]
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., car_setups: _Optional[_Iterable[_Union[CarSetupData, _Mapping]]] = ...) -> None: ...

class CarTelemetryData(_message.Message):
    __slots__ = ()
    SPEED_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_FIELD_NUMBER: _ClassVar[int]
    STEER_FIELD_NUMBER: _ClassVar[int]
    BRAKE_FIELD_NUMBER: _ClassVar[int]
    CLUTCH_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    ENGINE_RPM_FIELD_NUMBER: _ClassVar[int]
    DRS_FIELD_NUMBER: _ClassVar[int]
    REV_LIGHTS_PERCENT_FIELD_NUMBER: _ClassVar[int]
    REV_LIGHTS_BIT_VALUE_FIELD_NUMBER: _ClassVar[int]
    BRAKES_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TYRES_SURFACE_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TYRES_INNER_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TYRES_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_TYPE_FIELD_NUMBER: _ClassVar[int]
    speed: int
    throttle: float
    steer: float
    brake: float
    clutch: int
    gear: int
    engine_rpm: int
    drs: int
    rev_lights_percent: int
    rev_lights_bit_value: int
    brakes_temperature: _containers.RepeatedScalarFieldContainer[int]
    tyres_surface_temperature: _containers.RepeatedScalarFieldContainer[int]
    tyres_inner_temperature: _containers.RepeatedScalarFieldContainer[int]
    engine_temperature: int
    tyres_pressure: _containers.RepeatedScalarFieldContainer[float]
    surface_type: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, speed: _Optional[int] = ..., throttle: _Optional[float] = ..., steer: _Optional[float] = ..., brake: _Optional[float] = ..., clutch: _Optional[int] = ..., gear: _Optional[int] = ..., engine_rpm: _Optional[int] = ..., drs: _Optional[int] = ..., rev_lights_percent: _Optional[int] = ..., rev_lights_bit_value: _Optional[int] = ..., brakes_temperature: _Optional[_Iterable[int]] = ..., tyres_surface_temperature: _Optional[_Iterable[int]] = ..., tyres_inner_temperature: _Optional[_Iterable[int]] = ..., engine_temperature: _Optional[int] = ..., tyres_pressure: _Optional[_Iterable[float]] = ..., surface_type: _Optional[_Iterable[int]] = ...) -> None: ...

class PacketCarTelemetryData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAR_TELEMETRY_DATA_FIELD_NUMBER: _ClassVar[int]
    MFD_PANEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    MFD_PANEL_INDEX_SECONDARY_PLAYER_FIELD_NUMBER: _ClassVar[int]
    SUGGESTED_GEAR_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    car_telemetry_data: _containers.RepeatedCompositeFieldContainer[CarTelemetryData]
    mfd_panel_index: int
    mfd_panel_index_secondary_player: int
    suggested_gear: int
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., car_telemetry_data: _Optional[_Iterable[_Union[CarTelemetryData, _Mapping]]] = ..., mfd_panel_index: _Optional[int] = ..., mfd_panel_index_secondary_player: _Optional[int] = ..., suggested_gear: _Optional[int] = ...) -> None: ...

class CarStatusData(_message.Message):
    __slots__ = ()
    TRACTION_CONTROL_FIELD_NUMBER: _ClassVar[int]
    ANTI_LOCK_BRAKES_FIELD_NUMBER: _ClassVar[int]
    FUEL_MIX_FIELD_NUMBER: _ClassVar[int]
    FRONT_BRAKE_BIAS_FIELD_NUMBER: _ClassVar[int]
    PIT_LIMITER_STATUS_FIELD_NUMBER: _ClassVar[int]
    FUEL_IN_TANK_FIELD_NUMBER: _ClassVar[int]
    FUEL_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    FUEL_REMAINING_LAPS_FIELD_NUMBER: _ClassVar[int]
    MAX_RPM_FIELD_NUMBER: _ClassVar[int]
    IDLE_RPM_FIELD_NUMBER: _ClassVar[int]
    MAX_GEARS_FIELD_NUMBER: _ClassVar[int]
    DRS_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    DRS_ACTIVATION_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_TYRE_COMPOUND_FIELD_NUMBER: _ClassVar[int]
    VISUAL_TYRE_COMPOUND_FIELD_NUMBER: _ClassVar[int]
    TYRES_AGE_LAPS_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_FIA_FLAGS_FIELD_NUMBER: _ClassVar[int]
    ENGINE_POWER_ICE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_POWER_MGUK_FIELD_NUMBER: _ClassVar[int]
    ERS_STORE_ENERGY_FIELD_NUMBER: _ClassVar[int]
    ERS_DEPLOY_MODE_FIELD_NUMBER: _ClassVar[int]
    ERS_HARVESTED_THIS_LAP_MGUK_FIELD_NUMBER: _ClassVar[int]
    ERS_HARVESTED_THIS_LAP_MGUH_FIELD_NUMBER: _ClassVar[int]
    ERS_DEPLOYED_THIS_LAP_FIELD_NUMBER: _ClassVar[int]
    NETWORK_PAUSED_FIELD_NUMBER: _ClassVar[int]
    traction_control: int
    anti_lock_brakes: int
    fuel_mix: int
    front_brake_bias: int
    pit_limiter_status: int
    fuel_in_tank: float
    fuel_capacity: float
    fuel_remaining_laps: float
    max_rpm: int
    idle_rpm: int
    max_gears: int
    drs_allowed: int
    drs_activation_distance: int
    actual_tyre_compound: int
    visual_tyre_compound: int
    tyres_age_laps: int
    vehicle_fia_flags: int
    engine_power_ice: float
    engine_power_mguk: float
    ers_store_energy: float
    ers_deploy_mode: int
    ers_harvested_this_lap_mguk: float
    ers_harvested_this_lap_mguh: float
    ers_deployed_this_lap: float
    network_paused: int
    def __init__(self, traction_control: _Optional[int] = ..., anti_lock_brakes: _Optional[int] = ..., fuel_mix: _Optional[int] = ..., front_brake_bias: _Optional[int] = ..., pit_limiter_status: _Optional[int] = ..., fuel_in_tank: _Optional[float] = ..., fuel_capacity: _Optional[float] = ..., fuel_remaining_laps: _Optional[float] = ..., max_rpm: _Optional[int] = ..., idle_rpm: _Optional[int] = ..., max_gears: _Optional[int] = ..., drs_allowed: _Optional[int] = ..., drs_activation_distance: _Optional[int] = ..., actual_tyre_compound: _Optional[int] = ..., visual_tyre_compound: _Optional[int] = ..., tyres_age_laps: _Optional[int] = ..., vehicle_fia_flags: _Optional[int] = ..., engine_power_ice: _Optional[float] = ..., engine_power_mguk: _Optional[float] = ..., ers_store_energy: _Optional[float] = ..., ers_deploy_mode: _Optional[int] = ..., ers_harvested_this_lap_mguk: _Optional[float] = ..., ers_harvested_this_lap_mguh: _Optional[float] = ..., ers_deployed_this_lap: _Optional[float] = ..., network_paused: _Optional[int] = ...) -> None: ...

class PacketCarStatusData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAR_STATUS_DATA_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    car_status_data: _containers.RepeatedCompositeFieldContainer[CarStatusData]
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., car_status_data: _Optional[_Iterable[_Union[CarStatusData, _Mapping]]] = ...) -> None: ...

class FinalClassificationData(_message.Message):
    __slots__ = ()
    POSITION_FIELD_NUMBER: _ClassVar[int]
    NUM_LAPS_FIELD_NUMBER: _ClassVar[int]
    GRID_POSITION_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    NUM_PIT_STOPS_FIELD_NUMBER: _ClassVar[int]
    RESULT_STATUS_FIELD_NUMBER: _ClassVar[int]
    BEST_LAP_TIME_IN_MS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_RACE_TIME_FIELD_NUMBER: _ClassVar[int]
    PENALTIES_TIME_FIELD_NUMBER: _ClassVar[int]
    NUM_PENALTIES_FIELD_NUMBER: _ClassVar[int]
    NUM_TYRE_STINTS_FIELD_NUMBER: _ClassVar[int]
    TYRE_STINTS_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    TYRE_STINTS_VISUAL_FIELD_NUMBER: _ClassVar[int]
    TYRE_STINTS_END_LAPS_FIELD_NUMBER: _ClassVar[int]
    position: int
    num_laps: int
    grid_position: int
    points: int
    num_pit_stops: int
    result_status: int
    best_lap_time_in_ms: int
    total_race_time: float
    penalties_time: int
    num_penalties: int
    num_tyre_stints: int
    tyre_stints_actual: _containers.RepeatedScalarFieldContainer[int]
    tyre_stints_visual: _containers.RepeatedScalarFieldContainer[int]
    tyre_stints_end_laps: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, position: _Optional[int] = ..., num_laps: _Optional[int] = ..., grid_position: _Optional[int] = ..., points: _Optional[int] = ..., num_pit_stops: _Optional[int] = ..., result_status: _Optional[int] = ..., best_lap_time_in_ms: _Optional[int] = ..., total_race_time: _Optional[float] = ..., penalties_time: _Optional[int] = ..., num_penalties: _Optional[int] = ..., num_tyre_stints: _Optional[int] = ..., tyre_stints_actual: _Optional[_Iterable[int]] = ..., tyre_stints_visual: _Optional[_Iterable[int]] = ..., tyre_stints_end_laps: _Optional[_Iterable[int]] = ...) -> None: ...

class PacketFinalClassificationData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NUM_CARS_FIELD_NUMBER: _ClassVar[int]
    CLASSIFICATION_DATA_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    num_cars: int
    classification_data: _containers.RepeatedCompositeFieldContainer[FinalClassificationData]
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., num_cars: _Optional[int] = ..., classification_data: _Optional[_Iterable[_Union[FinalClassificationData, _Mapping]]] = ...) -> None: ...

class LobbyInfoData(_message.Message):
    __slots__ = ()
    AI_CONTROLLED_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NATIONALITY_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAR_NUMBER_FIELD_NUMBER: _ClassVar[int]
    READY_STATUS_FIELD_NUMBER: _ClassVar[int]
    ai_controlled: int
    team_id: int
    nationality: int
    platform: int
    name: str
    car_number: int
    ready_status: int
    def __init__(self, ai_controlled: _Optional[int] = ..., team_id: _Optional[int] = ..., nationality: _Optional[int] = ..., platform: _Optional[int] = ..., name: _Optional[str] = ..., car_number: _Optional[int] = ..., ready_status: _Optional[int] = ...) -> None: ...

class PacketLobbyInfoData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NUM_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    LOBBY_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    num_players: int
    lobby_players: _containers.RepeatedCompositeFieldContainer[LobbyInfoData]
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., num_players: _Optional[int] = ..., lobby_players: _Optional[_Iterable[_Union[LobbyInfoData, _Mapping]]] = ...) -> None: ...

class CarDamageData(_message.Message):
    __slots__ = ()
    TYRES_WEAR_FIELD_NUMBER: _ClassVar[int]
    TYRES_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    BRAKES_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    FRONT_LEFT_WING_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    FRONT_RIGHT_WING_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    REAR_WING_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    FLOOR_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    DIFFUSER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    SIDEPOD_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    DRS_FAULT_FIELD_NUMBER: _ClassVar[int]
    ERS_FAULT_FIELD_NUMBER: _ClassVar[int]
    GEAR_BOX_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_MGUH_WEAR_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ES_WEAR_FIELD_NUMBER: _ClassVar[int]
    ENGINE_CE_WEAR_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ICE_WEAR_FIELD_NUMBER: _ClassVar[int]
    ENGINE_MGUK_WEAR_FIELD_NUMBER: _ClassVar[int]
    ENGINE_TC_WEAR_FIELD_NUMBER: _ClassVar[int]
    ENGINE_BLOWN_FIELD_NUMBER: _ClassVar[int]
    ENGINE_SEIZED_FIELD_NUMBER: _ClassVar[int]
    tyres_wear: _containers.RepeatedScalarFieldContainer[float]
    tyres_damage: _containers.RepeatedScalarFieldContainer[int]
    brakes_damage: _containers.RepeatedScalarFieldContainer[int]
    front_left_wing_damage: int
    front_right_wing_damage: int
    rear_wing_damage: int
    floor_damage: int
    diffuser_damage: int
    sidepod_damage: int
    drs_fault: int
    ers_fault: int
    gear_box_damage: int
    engine_damage: int
    engine_mguh_wear: int
    engine_es_wear: int
    engine_ce_wear: int
    engine_ice_wear: int
    engine_mguk_wear: int
    engine_tc_wear: int
    engine_blown: int
    engine_seized: int
    def __init__(self, tyres_wear: _Optional[_Iterable[float]] = ..., tyres_damage: _Optional[_Iterable[int]] = ..., brakes_damage: _Optional[_Iterable[int]] = ..., front_left_wing_damage: _Optional[int] = ..., front_right_wing_damage: _Optional[int] = ..., rear_wing_damage: _Optional[int] = ..., floor_damage: _Optional[int] = ..., diffuser_damage: _Optional[int] = ..., sidepod_damage: _Optional[int] = ..., drs_fault: _Optional[int] = ..., ers_fault: _Optional[int] = ..., gear_box_damage: _Optional[int] = ..., engine_damage: _Optional[int] = ..., engine_mguh_wear: _Optional[int] = ..., engine_es_wear: _Optional[int] = ..., engine_ce_wear: _Optional[int] = ..., engine_ice_wear: _Optional[int] = ..., engine_mguk_wear: _Optional[int] = ..., engine_tc_wear: _Optional[int] = ..., engine_blown: _Optional[int] = ..., engine_seized: _Optional[int] = ...) -> None: ...

class PacketCarDamageData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAR_DAMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    car_damage_data: _containers.RepeatedCompositeFieldContainer[CarDamageData]
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., car_damage_data: _Optional[_Iterable[_Union[CarDamageData, _Mapping]]] = ...) -> None: ...

class LapHistoryData(_message.Message):
    __slots__ = ()
    LAP_TIME_IN_MS_FIELD_NUMBER: _ClassVar[int]
    SECTOR1_TIME_IN_MS_FIELD_NUMBER: _ClassVar[int]
    SECTOR1_TIME_MINUTES_FIELD_NUMBER: _ClassVar[int]
    SECTOR2_TIME_IN_MS_FIELD_NUMBER: _ClassVar[int]
    SECTOR2_TIME_MINUTES_FIELD_NUMBER: _ClassVar[int]
    SECTOR3_TIME_IN_MS_FIELD_NUMBER: _ClassVar[int]
    SECTOR3_TIME_MINUTES_FIELD_NUMBER: _ClassVar[int]
    LAP_VALID_BIT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    lap_time_in_ms: int
    sector1_time_in_ms: int
    sector1_time_minutes: int
    sector2_time_in_ms: int
    sector2_time_minutes: int
    sector3_time_in_ms: int
    sector3_time_minutes: int
    lap_valid_bit_flags: int
    def __init__(self, lap_time_in_ms: _Optional[int] = ..., sector1_time_in_ms: _Optional[int] = ..., sector1_time_minutes: _Optional[int] = ..., sector2_time_in_ms: _Optional[int] = ..., sector2_time_minutes: _Optional[int] = ..., sector3_time_in_ms: _Optional[int] = ..., sector3_time_minutes: _Optional[int] = ..., lap_valid_bit_flags: _Optional[int] = ...) -> None: ...

class TyreStintHistoryData(_message.Message):
    __slots__ = ()
    END_LAP_FIELD_NUMBER: _ClassVar[int]
    TYRE_ACTUAL_COMPOUND_FIELD_NUMBER: _ClassVar[int]
    TYRE_VISUAL_COMPOUND_FIELD_NUMBER: _ClassVar[int]
    end_lap: int
    tyre_actual_compound: int
    tyre_visual_compound: int
    def __init__(self, end_lap: _Optional[int] = ..., tyre_actual_compound: _Optional[int] = ..., tyre_visual_compound: _Optional[int] = ...) -> None: ...

class PacketSessionHistoryData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAR_IDX_FIELD_NUMBER: _ClassVar[int]
    NUM_LAPS_FIELD_NUMBER: _ClassVar[int]
    NUM_TYRE_STINTS_FIELD_NUMBER: _ClassVar[int]
    BEST_LAP_TIME_LAP_NUM_FIELD_NUMBER: _ClassVar[int]
    BEST_SECTOR1_LAP_NUM_FIELD_NUMBER: _ClassVar[int]
    BEST_SECTOR2_LAP_NUM_FIELD_NUMBER: _ClassVar[int]
    BEST_SECTOR3_LAP_NUM_FIELD_NUMBER: _ClassVar[int]
    LAP_HISTORY_DATA_FIELD_NUMBER: _ClassVar[int]
    TYRE_STINTS_HISTORY_DATA_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    car_idx: int
    num_laps: int
    num_tyre_stints: int
    best_lap_time_lap_num: int
    best_sector1_lap_num: int
    best_sector2_lap_num: int
    best_sector3_lap_num: int
    lap_history_data: _containers.RepeatedCompositeFieldContainer[LapHistoryData]
    tyre_stints_history_data: _containers.RepeatedCompositeFieldContainer[TyreStintHistoryData]
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., car_idx: _Optional[int] = ..., num_laps: _Optional[int] = ..., num_tyre_stints: _Optional[int] = ..., best_lap_time_lap_num: _Optional[int] = ..., best_sector1_lap_num: _Optional[int] = ..., best_sector2_lap_num: _Optional[int] = ..., best_sector3_lap_num: _Optional[int] = ..., lap_history_data: _Optional[_Iterable[_Union[LapHistoryData, _Mapping]]] = ..., tyre_stints_history_data: _Optional[_Iterable[_Union[TyreStintHistoryData, _Mapping]]] = ...) -> None: ...

class TyreSetData(_message.Message):
    __slots__ = ()
    ACTUAL_TYRE_COMPOUND_FIELD_NUMBER: _ClassVar[int]
    VISUAL_TYRE_COMPOUND_FIELD_NUMBER: _ClassVar[int]
    WEAR_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    RECOMMENDED_SESSION_FIELD_NUMBER: _ClassVar[int]
    LIFE_SPAN_FIELD_NUMBER: _ClassVar[int]
    USABLE_LIFE_FIELD_NUMBER: _ClassVar[int]
    LAP_DELTA_TIME_FIELD_NUMBER: _ClassVar[int]
    FITTED_FIELD_NUMBER: _ClassVar[int]
    actual_tyre_compound: int
    visual_tyre_compound: int
    wear: int
    available: int
    recommended_session: int
    life_span: int
    usable_life: int
    lap_delta_time: int
    fitted: int
    def __init__(self, actual_tyre_compound: _Optional[int] = ..., visual_tyre_compound: _Optional[int] = ..., wear: _Optional[int] = ..., available: _Optional[int] = ..., recommended_session: _Optional[int] = ..., life_span: _Optional[int] = ..., usable_life: _Optional[int] = ..., lap_delta_time: _Optional[int] = ..., fitted: _Optional[int] = ...) -> None: ...

class PacketTyreSetsData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAR_IDX_FIELD_NUMBER: _ClassVar[int]
    TYRE_SET_DATA_FIELD_NUMBER: _ClassVar[int]
    FITTED_IDX_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    car_idx: int
    tyre_set_data: _containers.RepeatedCompositeFieldContainer[TyreSetData]
    fitted_idx: int
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., car_idx: _Optional[int] = ..., tyre_set_data: _Optional[_Iterable[_Union[TyreSetData, _Mapping]]] = ..., fitted_idx: _Optional[int] = ...) -> None: ...

class PacketMotionExData(_message.Message):
    __slots__ = ()
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUSPENSION_POSITION_FIELD_NUMBER: _ClassVar[int]
    SUSPENSION_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    SUSPENSION_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    WHEEL_SPEED_FIELD_NUMBER: _ClassVar[int]
    WHEEL_SLIP_RATIO_FIELD_NUMBER: _ClassVar[int]
    WHEEL_SLIP_ANGLE_FIELD_NUMBER: _ClassVar[int]
    WHEEL_LAT_FORCE_FIELD_NUMBER: _ClassVar[int]
    WHEEL_LONG_FORCE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_OF_COG_ABOVE_GROUND_FIELD_NUMBER: _ClassVar[int]
    LOCAL_VELOCITY_X_FIELD_NUMBER: _ClassVar[int]
    LOCAL_VELOCITY_Y_FIELD_NUMBER: _ClassVar[int]
    LOCAL_VELOCITY_Z_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_X_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_Y_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_Z_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_ACCELERATION_X_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_ACCELERATION_Y_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_ACCELERATION_Z_FIELD_NUMBER: _ClassVar[int]
    FRONT_WHEELS_ANGLE_FIELD_NUMBER: _ClassVar[int]
    WHEEL_VERT_FORCE_FIELD_NUMBER: _ClassVar[int]
    header: PacketHeader
    suspension_position: _containers.RepeatedScalarFieldContainer[float]
    suspension_velocity: _containers.RepeatedScalarFieldContainer[float]
    suspension_acceleration: _containers.RepeatedScalarFieldContainer[float]
    wheel_speed: _containers.RepeatedScalarFieldContainer[float]
    wheel_slip_ratio: _containers.RepeatedScalarFieldContainer[float]
    wheel_slip_angle: _containers.RepeatedScalarFieldContainer[float]
    wheel_lat_force: _containers.RepeatedScalarFieldContainer[float]
    wheel_long_force: _containers.RepeatedScalarFieldContainer[float]
    height_of_cog_above_ground: float
    local_velocity_x: float
    local_velocity_y: float
    local_velocity_z: float
    angular_velocity_x: float
    angular_velocity_y: float
    angular_velocity_z: float
    angular_acceleration_x: float
    angular_acceleration_y: float
    angular_acceleration_z: float
    front_wheels_angle: float
    wheel_vert_force: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[PacketHeader, _Mapping]] = ..., suspension_position: _Optional[_Iterable[float]] = ..., suspension_velocity: _Optional[_Iterable[float]] = ..., suspension_acceleration: _Optional[_Iterable[float]] = ..., wheel_speed: _Optional[_Iterable[float]] = ..., wheel_slip_ratio: _Optional[_Iterable[float]] = ..., wheel_slip_angle: _Optional[_Iterable[float]] = ..., wheel_lat_force: _Optional[_Iterable[float]] = ..., wheel_long_force: _Optional[_Iterable[float]] = ..., height_of_cog_above_ground: _Optional[float] = ..., local_velocity_x: _Optional[float] = ..., local_velocity_y: _Optional[float] = ..., local_velocity_z: _Optional[float] = ..., angular_velocity_x: _Optional[float] = ..., angular_velocity_y: _Optional[float] = ..., angular_velocity_z: _Optional[float] = ..., angular_acceleration_x: _Optional[float] = ..., angular_acceleration_y: _Optional[float] = ..., angular_acceleration_z: _Optional[float] = ..., front_wheels_angle: _Optional[float] = ..., wheel_vert_force: _Optional[_Iterable[float]] = ...) -> None: ...
