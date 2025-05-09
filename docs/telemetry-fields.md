# F1 Telemetry Data Checklist (Single Car / Session Focus)

This checklist is to help select relevant data points for a telemetry dashboard. We will focus on data pertaining to a single selected car (e.g., the player car, identified by `player_car_index` in the header) or session-wide information.

## I. Packet Header (Common to all packets)

This information is crucial for context and data integrity.

- [ ] `packet_format` - Game year of the packet format (e.g., 2023)
- [ ] `game_year` - Year of the game (e.g., 23 for F1 23)
- [ ] `game_major_version` - Game major version
- [ ] `game_minor_version` - Game minor version
- [ ] `packet_version` - Version of this packet type
- [x] `packet_id` - Identifier for the packet type (e.g., 0 = Motion, 1 = Session, etc.)
- [ ] `session_uid` - Unique identifier for the session (convert to string for JSON)
- [x] `session_time` - Session timestamp in seconds
- [ ] `frame_identifier` - Identifier for the frame the data was retrieved on
- [ ] `overall_frame_identifier` - Overall identifier for the frame, including paused games
- [x] `player_car_index` - Index of the player's car in the arrays
- [ ] `secondary_player_car_index` - Index of the secondary player's car (255 if no second player)

## II. Participant Data (For a selected car)

Data identifying a specific participant. You'd typically filter the `m_participants` array by `player_car_index` or another chosen index.

- [ ] `m_aiControlled` - Whether the vehicle is AI (1) or Human (0) controlled
- [ ] `m_driverId` - Driver ID (see F1 game appendix for mapping, 255 if network human)
- [ ] `m_networkId` - Network ID – unique identifier for network players
- [ ] `m_teamId` - Team ID (see F1 game appendix for mapping)
- [ ] `m_myTeam` - My Team flag – 1 if this car is part of player's "My Team", 0 otherwise
- [ ] `m_raceNumber` - Race number of the car
- [ ] `m_nationality` - Nationality of the driver (see F1 game appendix)
- [ ] `m_name` - Name of the participant (UTF-8 format)
- [ ] `m_yourTelemetry` - Your telemetry visibility: 0 = restricted, 1 = public
- [ ] `m_showOnlineNames` - Whether to show online names (1) or not (0)
- [ ] `m_platform` - Gaming platform: 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown

## III. Car Setup Data (For a selected car)

Detailed setup of a specific car. Filter `m_carSetups` array.

- [ ] `m_frontWing` - Front wing aero setting
- [ ] `m_rearWing` - Rear wing aero setting
- [ ] `m_onThrottle` - Differential adjustment on throttle (percentage)
- [ ] `m_offThrottle` - Differential adjustment off throttle (percentage)
- [ ] `m_frontCamber` - Front camber angle (suspension geometry)
- [ ] `m_rearCamber` - Rear camber angle (suspension geometry)
- [ ] `m_frontToe` - Front toe angle (suspension geometry)
- [ ] `m_rearToe` - Rear toe angle (suspension geometry)
- [ ] `m_frontSuspension` - Front suspension stiffness
- [ ] `m_rearSuspension` - Rear suspension stiffness
- [ ] `m_frontAntiRollBar` - Front anti-roll bar stiffness
- [ ] `m_rearAntiRollBar` - Rear anti-roll bar stiffness (comment typo: should be Rear anti-roll bar)
- [ ] `m_frontSuspensionHeight` - Front ride height
- [ ] `m_rearSuspensionHeight` - Rear ride height
- [ ] `m_brakePressure` - Brake pressure (percentage)
- [ ] `m_brakeBias` - Brake bias (percentage, front)
- [ ] `m_rearLeftTyrePressure` - Rear left tyre pressure (PSI)
- [ ] `m_rearRightTyrePressure` - Rear right tyre pressure (PSI)
- [ ] `m_frontLeftTyrePressure` - Front left tyre pressure (PSI)
- [ ] `m_frontRightTyrePressure` - Front right tyre pressure (PSI)
- [ ] `m_ballast` - Ballast adjustment
- [ ] `m_fuelLoad` - Fuel load in kilograms

## IV. Car Telemetry Data (For a selected car)

Real-time telemetry from a specific car. Filter `m_carTelemetryData` array.

- [x] `m_speed` - Speed of car in kilometres per hour
- [x] `m_throttle` - Amount of throttle applied (0.0 to 1.0)
- [x] `m_steer` - Steering input (-1.0 full lock left to 1.0 full lock right)
- [x] `m_brake` - Amount of brake applied (0.0 to 1.0)
- [x] `m_clutch` - Amount of clutch applied (0 to 100)
- [x] `m_gear` - Gear selected (1-8, N=0, R=-1)
- [x] `m_engineRPM` - Engine RPM
- [x] `m_drs` - DRS status: 0 = off, 1 = on
- [ ] `m_revLightsPercent` - Rev lights indicator (percentage)
- [ ] `m_revLightsBitValue` - Rev lights (bit 0 = leftmost LED, bit 14 = rightmost LED)
- [x] `m_brakesTemperature` - Array of brakes temperature (Celsius) [RL, RR, FL, FR]
- [x] `m_tyresSurfaceTemperature` - Array of tyres surface temperature (Celsius) [RL, RR, FL, FR]
- [x] `m_tyresInnerTemperature` - Array of tyres inner temperature (Celsius) [RL, RR, FL, FR]
- [x] `m_engineTemperature` - Engine temperature (Celsius)
- [x] `m_tyresPressure` - Array of tyres pressure (PSI) [RL, RR, FL, FR]
- [x] `m_surfaceType` - Array of driving surface type for each wheel (see F1 game appendix) [RL, RR, FL, FR]

### From PacketCarTelemetryData (Player/Session specific, not per-car array)

- [ ] `m_mfdPanelIndex` - Index of MFD panel open for player (255 = MFD closed)
- [ ] `m_mfdPanelIndexSecondaryPlayer` - Index of MFD panel open for secondary player
- [ ] `m_suggestedGear` - Suggested gear for the player (1-8, 0 if no suggestion)

## V. Car Status Data (For a selected car)

Status information for a specific car. Filter `m_car_status_data` array.

- [ ] `m_traction_control` - Traction control level: 0 = off, 1 = medium, 2 = full
- [ ] `m_anti_lock_brakes` - Anti-lock brakes status: 0 = off, 1 = on
- [ ] `m_fuel_mix` - Fuel mix: 0 = lean, 1 = standard, 2 = rich, 3 = max
- [ ] `m_front_brake_bias` - Front brake bias (percentage)
- [ ] `m_pit_limiter_status` - Pit limiter status: 0 = off, 1 = on
- [ ] `m_fuel_in_tank` - Current fuel mass in kilograms
- [ ] `m_fuel_capacity` - Fuel capacity in kilograms
- [ ] `m_fuel_remaining_laps` - Fuel remaining in terms of laps (value from MFD)
- [ ] `m_max_rpm` - Car's maximum RPM (point of rev limiter)
- [ ] `m_idle_rpm` - Car's idle RPM
- [ ] `m_max_gears` - Maximum number of gears for this car
- [ ] `m_drs_allowed` - DRS allowed status: 0 = not allowed, 1 = allowed, -1 = unknown
- [ ] `m_drs_activation_distance` - Distance where DRS will be available (meters); 0 if not available soon
- [ ] `m_actual_tyre_compound` - Actual tyre compound (see F1 game appendix for mapping, e.g., F1 Modern: 16=C5... 7=Inter, 8=Wet)
- [ ] `m_visual_tyre_compound` - Visual tyre compound (see F1 game appendix, can differ from actual)
- [ ] `m_tyres_age_laps` - Age in laps of the current set of tyres
- [ ] `m_vehicle_fia_flags` - Vehicle FIA flags: -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
- [ ] `m_engine_power_ice` - Engine power output of ICE (Internal Combustion Engine) in Watts
- [ ] `m_engine_power_mguk` - Engine power output of MGU-K (Motor Generator Unit - Kinetic) in Watts
- [ ] `m_ers_store_energy` - ERS (Energy Recovery System) energy store in Joules
- [ ] `m_ers_deploy_mode` - ERS deployment mode: 0 = none, 1 = medium, 2 = hotlap, 3 = overtake
- [ ] `m_ers_harvested_this_lap_mguk` - ERS energy harvested this lap by MGU-K (Joules)
- [ ] `m_ers_harvested_this_lap_mguh` - ERS energy harvested this lap by MGU-H (Motor Generator Unit - Heat) (Joules)
- [ ] `m_ers_deployed_this_lap` - ERS energy deployed this lap (Joules)
- [ ] `m_network_paused` - Whether the car is paused in a network game: 0 = not paused, 1 = paused

## VI. Car Motion Data (For a selected car)

World space motion data for a specific car. Filter `m_carMotionData` array.

- [ ] `m_worldPositionX` - World space X position (metres)
- [ ] `m_worldPositionY` - World space Y position (metres)
- [ ] `m_worldPositionZ` - World space Z position (metres)
- [ ] `m_worldVelocityX` - Velocity in world space X (metres/second)
- [ ] `m_worldVelocityY` - Velocity in world space Y (metres/second)
- [ ] `m_worldVelocityZ` - Velocity in world space Z (metres/second)
- [ ] `m_worldForwardDirX` - World space forward X direction (normalised)
- [ ] `m_worldForwardDirY` - World space forward Y direction (normalised)
- [ ] `m_worldForwardDirZ` - World space forward Z direction (normalised)
- [ ] `m_worldRightDirX` - World space right X direction (normalised)
- [ ] `m_worldRightDirY` - World space right Y direction (normalised)
- [ ] `m_worldRightDirZ` - World space right Z direction (normalised)
- [ ] `m_gForceLateral` - Lateral G-force
- [ ] `m_gForceLongitudinal` - Longitudinal G-force
- [ ] `m_gForceVertical` - Vertical G-force
- [ ] `m_yaw` - Yaw angle in radians
- [ ] `m_pitch` - Pitch angle in radians
- [ ] `m_roll` - Roll angle in radians

## VII. Lap Data (For a selected car)

Lap timing and status for a specific car. Filter `m_lapData` array.

- [ ] `m_lastLapTimeInMS` - Last lap time in milliseconds
- [ ] `m_currentLapTimeInMS` - Current lap time in milliseconds
- [ ] `m_sector1TimeInMS` - Sector 1 time for current lap in milliseconds ( stazione for current lap)
- [ ] `m_sector1TimeMinutes` - Sector 1 whole minute part for current lap
- [ ] `m_sector2TimeInMS` - Sector 2 time for current lap in milliseconds
- [ ] `m_sector2TimeMinutes` - Sector 2 whole minute part for current lap
- [ ] `m_deltaToCarInFrontInMS` - Delta to car in front in milliseconds
- [ ] `m_deltaToRaceLeaderInMS` - Delta to race leader in milliseconds
- [ ] `m_lapDistance` - Distance covered on current lap in metres
- [ ] `m_totalDistance` - Total distance covered in session in metres
- [ ] `m_safetyCarDelta` - Delta to safety car in seconds (if active)
- [ ] `m_carPosition` - Car's current race position
- [ ] `m_currentLapNum` - Current lap number
- [ ] `m_pitStatus` - Pit status: 0 = none, 1 = pitting, 2 = in pit area
- [ ] `m_numPitStops` - Number of pit stops made
- [ ] `m_sector` - Current sector (0 = sector1, 1 = sector2, 2 = sector3)
- [ ] `m_currentLapInvalid` - Current lap invalid: 0 = valid, 1 = invalid
- [ ] `m_penalties` - Accumulated_penalties in seconds
- [ ] `m_totalWarnings` - Total number of warnings received
- [ ] `m_cornerCuttingWarnings` - Number of corner cutting warnings
- [ ] `m_numUnservedDriveThroughPens` - Number of unserved drive-through penalties
- [ ] `m_numUnservedStopGoPens` - Number of unserved stop-go penalties
- [ ] `m_gridPosition` - Grid position at the start of the race
- [ ] `m_driverStatus` - Driver status: 0 = in garage, 1 = flying lap, 2 = in lap, 3 = out lap, 4 = on track
- [ ] `m_resultStatus` - Result status: 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = DNF, 5 = DSQ, 6 = Not Classified, 7 = Retired
- [ ] `m_pitLaneTimerActive` - Pit lane timer active: 0 = no, 1 = yes
- [ ] `m_pitLaneTimeInLaneInMS` - Time spent in pit lane in milliseconds
- [ ] `m_pitStopTimerInMS` - Time spent stationary in pit stop in milliseconds
- [ ] `m_pitStopShouldServePen` - Whether the car should serve a penalty during this pit stop: 0 = no, 1 = yes

### From PacketLapData (Time Trial specific)
- [ ] `m_timeTrialPBCarIdx` - Index of the car that is the personal best in a time trial
- [ ] `m_timeTrialRivalCarIdx` - Index of the car that is the rival in a time trial

## VIII. Car Damage Data (For a selected car)

Damage status for a specific car. Filter `m_car_damage_data` array.

- [ ] `m_tyres_wear` - Array of tyre wear (percentage) [RL, RR, FL, FR]
- [ ] `m_tyres_damage` - Array of tyre damage (percentage) [RL, RR, FL, FR] (0-100, higher is worse)
- [ ] `m_brakes_damage` - Array of brakes damage (percentage) [RL, RR, FL, FR]
- [ ] `m_front_left_wing_damage` - Front left wing damage (percentage)
- [ ] `m_front_right_wing_damage` - Front right wing damage (percentage)
- [ ] `m_rear_wing_damage` - Rear wing damage (percentage)
- [ ] `m_floor_damage` - Floor damage (percentage)
- [ ] `m_diffuser_damage` - Diffuser damage (percentage)
- [ ] `m_sidepod_damage` - Sidepod damage (percentage)
- [ ] `m_drs_fault` - DRS fault indicator: 0 = OK, 1 = fault
- [ ] `m_ers_fault` - ERS fault indicator: 0 = OK, 1 = fault
- [ ] `m_gear_box_damage` - Gear box damage (percentage)
- [ ] `m_engine_damage` - Engine overall damage (percentage)
- [ ] `m_engine_mguh_wear` - Engine MGU-H wear (percentage)
- [ ] `m_engine_es_wear` - Engine ES (Energy Store) wear (percentage)
- [ ] `m_engine_ce_wear` - Engine CE (Control Electronics) wear (percentage)
- [ ] `m_engine_ice_wear` - Engine ICE (Internal Combustion Engine) wear (percentage)
- [ ] `m_engine_mguk_wear` - Engine MGU-K wear (percentage)
- [ ] `m_engine_tc_wear` - Engine TC (Turbo Charger) wear (percentage)
- [ ] `m_engine_blown` - Engine blown status: 0 = OK, 1 = fault (blown)
- [ ] `m_engine_seized` - Engine seized status: 0 = OK, 1 = fault (seized)

## IX. Session History Data (For a selected car)

Lap history and tyre stint history for a *single car*, identified by `m_carIdx` in `PacketSessionHistoryData`.

- [ ] `m_carIdx` (from PacketSessionHistoryData) - Index of the car this lap/stint data relates to.
- [ ] `m_numLaps` (from PacketSessionHistoryData) - Number of laps in the history data (including current partial lap).
- [ ] `m_numTyreStints` (from PacketSessionHistoryData) - Number of tyre stints in the history data.
- [ ] `m_bestLapTimeLapNum` (from PacketSessionHistoryData) - Lap number on which the best lap time was achieved.
- [ ] `m_bestSector1LapNum` (from PacketSessionHistoryData) - Lap number on which the best Sector 1 time was achieved.
- [ ] `m_bestSector2LapNum` (from PacketSessionHistoryData) - Lap number on which the best Sector 2 time was achieved.
- [ ] `m_bestSector3LapNum` (from PacketSessionHistoryData) - Lap number on which the best Sector 3 time was achieved.

### Lap History Entry (within `m_lapHistoryData` array for the selected car)

- [ ] `m_lapTimeInMS` - Lap time in milliseconds
- [ ] `m_sector1TimeInMS` - Sector 1 time in milliseconds
- [ ] `m_sector1TimeMinutes` - Sector 1 whole minute part
- [ ] `m_sector2TimeInMS` - Sector 2 time in milliseconds
- [ ] `m_sector2TimeMinutes` - Sector 2 whole minute part
- [ ] `m_sector3TimeInMS` - Sector 3 time in milliseconds
- [ ] `m_sector3TimeMinutes` - Sector 3 whole minute part
- [ ] `m_lapValidBitFlags` - Lap/sector validity: 0x01=lap valid, 0x02=S1 valid, 0x04=S2 valid, 0x08=S3 valid

### Tyre Stint History Entry (within `m_tyreStintsHistoryData` array for the selected car)

- [ ] `m_endLap` - Lap the tyre usage ends on (255 if current tyre)
- [ ] `m_tyreActualCompound` - Actual tyre compound used during stint (see F1 game appendix)
- [ ] `m_tyreVisualCompound` - Visual tyre compound used during stint (see F1 game appendix)

## X. Tyre Sets Data (For a selected car)

Available tyre sets for a *single car*, identified by `m_carIdx` in `PacketTyreSetsData`.

- [ ] `m_carIdx` (from PacketTyreSetsData) - Index of the car this tyre set data relates to.
- [ ] `m_fittedIdx` (from PacketTyreSetsData) - Index in `m_tyreSetData` array of the currently fitted tyre set.

### Tyre Set Entry (within `m_tyreSetData` array for the selected car)

- [ ] `m_actualTyreCompound` - Actual tyre compound (see F1 game appendix)
- [ ] `m_visualTyreCompound` - Visual tyre compound (see F1 game appendix)
- [ ] `m_wear` - Tyre wear (percentage)
- [ ] `m_available` - Whether this set is currently available: 0 = no, 1 = yes
- [ ] `m_recommendedSession` - Recommended session for this tyre set (see F1 game appendix)
- [ ] `m_lifeSpan` - Laps left in this tyre set (estimated initial lifespan)
- [ ] `m_usableLife` - Max number of laps recommended for this compound (manufacturer's recommendation)
- [ ] `m_lapDeltaTime` - Lap delta time in milliseconds compared to fitted set (estimated performance difference)
- [ ] `m_fitted` - Whether the set is fitted or not: 0 = no, 1 = yes

## XI. Extended Motion Data (PacketMotionExData - For a selected car)

Detailed physics data, typically for the player's car or a specifically focused car.
*Note: The packet sends data for all cars. You would need to filter/select data for the car of interest, often using an index.*
The array fields below (e.g., `m_suspensionPosition`) are per-wheel for the selected car, in order [RL, RR, FL, FR].

- [ ] `m_suspensionPosition` - Array of suspension position for each wheel
- [ ] `m_suspensionVelocity` - Array of suspension velocity for each wheel
- [ ] `m_suspensionAcceleration` - Array of suspension acceleration for each wheel
- [ ] `m_wheelSpeed` - Array of speed of each wheel (metres/second)
- [ ] `m_wheelSlipRatio` - Array of slip ratio for each wheel (longitudinal slip)
- [ ] `m_wheelSlipAngle` - Array of slip angles for each wheel (lateral slip)
- [ ] `m_wheelLatForce` - Array of lateral forces for each wheel (Newtons)
- [ ] `m_wheelLongForce` - Array of longitudinal forces for each wheel (Newtons)
- [ ] `m_heightOfCOGAboveGround` - Height of Centre of Gravity above ground (metres)
- [ ] `m_localVelocityX` - Velocity in local car space X (metres/second, forward)
- [ ] `m_localVelocityY` - Velocity in local car space Y (metres/second, up)
- [ ] `m_localVelocityZ` - Velocity in local car space Z (metres/second, right)
- [ ] `m_angularVelocityX` - Angular velocity x-component (radians/second, roll)
- [ ] `m_angularVelocityY` - Angular velocity y-component (radians/second, pitch)
- [ ] `m_angularVelocityZ` - Angular velocity z-component (radians/second, yaw)
- [ ] `m_angularAccelerationX` - Angular acceleration x-component (radians/second^2, roll)
- [ ] `m_angularAccelerationY` - Angular acceleration y-component (radians/second^2, pitch)
- [ ] `m_angularAccelerationZ` - Angular acceleration z-component (radians/second^2, yaw)
- [ ] `m_frontWheelsAngle` - Current front wheels angle in radians (positive is right)
- [ ] `m_wheelVertForce` - Array of vertical forces on each wheel (Newtons)

## XII. Session Data (Overall Session Information)

This data is from `PacketSessionData` and is generally session-wide, not specific to one car unless indicated (e.g. spectator).

- [ ] `m_weather` - Weather type: 0=clear, 1=light cloud, 2=overcast, 3=light rain, 4=heavy rain, 5=storm
- [ ] `m_trackTemperature` - Track temperature in Celsius
- [ ] `m_airTemperature` - Air temperature in Celsius
- [ ] `m_totalLaps` - Total number of laps in this race
- [ ] `m_trackLength` - Track length in metres
- [ ] `m_sessionType` - Session type (see F1 game appendix, e.g., 0=unknown, 1=P1, ..., 10=Race)
- [ ] `m_trackId` - Identifier for the track (see F1 game appendix, -1 for unknown)
- [ ] `m_formula` - Formula type: 0=F1 Modern, 1=F1 Classic, 2=F2, 3=F1 Generic, 4=Beta, 5=Supercars, 6=Esports
- [ ] `m_sessionTimeLeft` - Session time left in seconds
- [ ] `m_sessionDuration` - Session duration in seconds
- [ ] `m_pitSpeedLimit` - Pit speed limit in km/h
- [ ] `m_gamePaused` - Whether the game is paused: 0 = not paused, 1 = paused
- [ ] `m_isSpectating` - Whether the player is spectating: 0 = no, 1 = yes
- [ ] `m_spectatorCarIndex` - Index of the car being spectated (if `m_isSpectating` is 1)
- [ ] `m_sliProNativeSupport` - SLI Pro support: 0 = inactive, 1 = active
- [ ] `m_numMarshalZones` - Number of marshal zones on track
- [ ] `m_safetyCarStatus` - Safety car status: 0=no SC, 1=full SC, 2=VSC, 3=formation lap
- [ ] `m_networkGame` - Network game: 0 = offline, 1 = online
- [ ] `m_numWeatherForecastSamples` - Number of weather forecast samples available
- [ ] `m_forecastAccuracy` - Forecast accuracy: 0 = perfect, 1 = approximate
- [ ] `m_aiDifficulty` - AI difficulty rating (0-110)
- [ ] `m_seasonLinkIdentifier` - Identifier for series (e.g., My Team, Online Championship)
- [ ] `m_weekendLinkIdentifier` - Identifier for weekend
- [ ] `m_sessionLinkIdentifier` - Identifier for session
- [ ] `m_pitStopWindowIdealLap` - Ideal lap for pit stop window
- [ ] `m_pitStopWindowLatestLap` - Latest lap for pit stop window
- [ ] `m_pitStopRejoinPosition` - Predicted position after pit stop
- [ ] `m_steeringAssist` - Steering assist enabled: 0 = no, 1 = yes
- [ ] `m_brakingAssist` - Braking assist enabled: 0 = no, 1 = yes
- [ ] `m_gearboxAssist` - Gearbox assist level (see F1 game appendix)
- [ ] `m_pitAssist` - Pit assist enabled: 0 = no, 1 = yes
- [ ] `m_pitReleaseAssist` - Pit release assist enabled: 0 = no, 1 = yes
- [ ] `m_ERSAssist` - ERS assist enabled: 0 = no, 1 = yes
- [ ] `m_DRSAssist` - DRS assist enabled: 0 = no, 1 = yes
- [ ] `m_dynamicRacingLine` - Dynamic racing line type (see F1 game appendix)
- [ ] `m_dynamicRacingLineType` - Dynamic racing line type: 0 = 2D, 1 = 3D
- [ ] `m_gameMode` - Game mode identifier (see F1 game appendix)
- [ ] `m_ruleSet` - Ruleset (e.g., practice/qualifying, race, time trial - see F1 game appendix)
- [ ] `m_timeOfDay` - Local time of day in minutes from midnight
- [ ] `m_sessionLength` - Session length: 0=None, 2=Very Short, 3=Short, 4=Medium, 5=Medium Long, 6=Long, 7=Full
- [ ] `m_speedUnitsLeadPlayer` - Speed units for lead player: 0 = MPH, 1 = KPH
- [ ] `m_temperatureUnitsLeadPlayer` - Temp units for lead player: 0 = Celsius, 1 = Fahrenheit
- [ ] `m_speedUnitsSecondaryPlayer` - Speed units for secondary player: 0 = MPH, 1 = KPH
- [ ] `m_temperatureUnitsSecondaryPlayer` - Temp units for secondary player: 0 = Celsius, 1 = Fahrenheit
- [ ] `m_numSafetyCarPeriods` - Number of safety car periods in this session
- [ ] `m_numVirtualSafetyCarPeriods` - Number of VSC periods in this session
- [ ] `m_numRedFlagPeriods` - Number of red flag periods in this session

### Marshal Zone Data (within `m_marshalZones` array of `PacketSessionData`)

- [ ] `m_zoneStart` - Fraction (0..1) of track where marshal zone starts
- [ ] `m_zoneFlag` - Flag waved at marshal zone: -1=Unknown, 0=None, 1=Green, 2=Blue, 3=Yellow, 4=Red

### Weather Forecast Sample (within `m_weatherForecastSamples` array of `PacketSessionData`)

- [ ] `m_sessionType` - Session type of the forecast (see F1 game appendix)
- [ ] `m_timeOffset` - Time offset in minutes from start of session for this forecast
- [ ] `m_weather` - Weather type forecast (see `m_weather` above for codes)
- [ ] `m_trackTemperature` - Track temperature forecast (Celsius)
- [ ] `m_trackTemperatureChange` - Track temp change: 0=Up, 1=Down, 2=No change
- [ ] `m_airTemperature` - Air temperature forecast (Celsius)
- [ ] `m_airTemperatureChange` - Air temp change: 0=Up, 1=Down, 2=No change
- [ ] `m_rainPercentage` - Rain percentage chance (0-100)

## XIII. Final Classification Data (For a selected car)

Post-session results for a specific car. Filter `m_classificationData` array.

- [ ] `m_position` - Finishing position
- [ ] `m_numLaps` - Number of laps completed
- [ ] `m_gridPosition` - Grid position of the car at start
- [ ] `m_points` - Number of points scored
- [ ] `m_numPitStops` - Number of pit stops made
- [ ] `m_resultStatus` - Result status (see LapData `m_resultStatus` for codes)
- [ ] `m_bestLapTimeInMS` - Best lap time of the session in milliseconds
- [ ] `m_totalRaceTime` - Total race time in seconds (minus penalties)
- [ ] `m_penaltiesTime` - Total penalties accumulated in seconds
- [ ] `m_numPenalties` - Number of penalties applied to this driver
- [ ] `m_numTyreStints` - Number of tyre stints completed
- [ ] `m_tyreStintsActual` - Array of actual tyre compounds used per stint (see F1 game appendix)
- [ ] `m_tyreStintsVisual` - Array of visual tyre compounds used per stint (see F1 game appendix)
- [ ] `m_tyreStintsEndLaps` - Array of lap numbers when each stint ended

### From PacketFinalClassificationData (Session specific)
- [ ] `m_numCars` - Number of cars in the final classification

## XIV. Lobby Info Data (For a selected player in lobby)

Information about a player in a pre-session lobby. Filter `m_lobbyPlayers` array.

- [ ] `m_aiControlled` - Whether the vehicle is AI (1) or Human (0) controlled
- [ ] `m_teamId` - Team ID (see F1 game appendix, 255 if no team selected)
- [ ] `m_nationality` - Nationality ID (see F1 game appendix)
- [ ] `m_platform` - Platform: 1 = Steam, 3 = PlayStation, 4 = Xbox, 6 = Origin, 255 = unknown
- [ ] `m_name` - Name of participant
- [ ] `m_carNumber` - Car number of the player
- [ ] `m_readyStatus` - Ready status: 0 = not ready, 1 = ready, 2 = spectating

### From PacketLobbyInfoData (Lobby specific)
- [ ] `m_numPlayers` - Number of players in the lobby data

## XV. Event Data (PacketEventData)

Events that occur during the session. The `m_eventDetails` field will vary based on `m_eventStringCode`.

- [ ] `m_eventStringCode` - String code identifying the event type (e.g., "SSTA" for Session Started, "FTLP" for Fastest Lap)

### If Event is 'FastestLap' (`FastestLapData`):
- [ ] `vehicleIdx` - Vehicle index of the car that set the fastest lap
- [ ] `lapTime` - Lap time in seconds

### If Event is 'Retirement' (`RetirementData`):
- [ ] `vehicleIdx` - Vehicle index of the retiring car

### If Event is 'TeamMateInPits' (`TeamMateInPitsData`):
- [ ] `vehicleIdx` - Vehicle index of the team mate in pits

### If Event is 'RaceWinner' (`RaceWinnerData`):
- [ ] `vehicleIdx` - Vehicle index of the race winner

### If Event is 'Penalty' (`PenaltyData`):
- [ ] `penaltyType` - Penalty type (see F1 game appendix)
- [ ] `infringementType` - Infringement type (see F1 game appendix)
- [ ] `vehicleIdx` - Vehicle index of the car penalized
- [ ] `otherVehicleIdx` - Vehicle index of other car involved (if any)
- [ ] `time` - Time gained or penalty time in seconds
- [ ] `lapNum` - Lap number of infringement
- [ ] `placesGained` - Number of places gained through infringement

### If Event is 'SpeedTrap' (`SpeedTrapData`):
- [ ] `vehicleIdx` - Vehicle index of the car triggering the speed trap
- [ ] `speed` - Speed in km/h
- [ ] `isOverallFastestInSession` - 1 if overall fastest in session, 0 otherwise
- [ ] `isDriverFastestInSession` - 1 if driver's fastest in session, 0 otherwise
- [ ] `fastestVehicleIdxInSession` - Vehicle index of the overall fastest car in session at this speed trap
- [ ] `fastestSpeedInSession` - Speed of the overall fastest car in session at this speed trap (km/h)

### If Event is 'StartLights' (`StartLightsData`):
- [ ] `numLights` - Number of lights lit on start gantry (0-5)

### If Event is 'DriveThroughPenaltyServed' (`DriveThroughPenaltyServedData`):
- [ ] `vehicleIdx` - Vehicle index of car serving drive-through

### If Event is 'StopGoPenaltyServed' (`StopGoPenaltyServedData`):
- [ ] `vehicleIdx` - Vehicle index of car serving stop-go

### If Event is 'Flashback' (`FlashbackData`):
- [ ] `flashbackFrameIdentifier` - Frame identifier when flashback was activated
- [ ] `flashbackSessionTime` - Session time when flashback was activated

### If Event is 'Buttons' (`ButtonsData`):
- [ ] `buttonStatus` - Bit flags for button presses (see F1 game appendix for mapping)

### If Event is 'Overtake' (`OvertakeData`):
- [ ] `overtakingVehicleIdx` - Vehicle index of the car performing the overtake
- [ ] `beingOvertakenVehicleIdx` - Vehicle index of the car being overtaken

---

This list should give you a comprehensive starting point for your discussion! Good luck.
