export type PacketHeader = {
  gameYear: number;
  packetId: string;
  sessionUid: string;
  sessionTime: string;
  playerCarIndex: number;
};

export type CarMotion = {
  worldPositionX: number;
  worldPositionY: number;
  worldPositionZ: number;
};

export type PacketMotionData = {
  header: PacketHeader;
  cars: CarMotion[];

  layer1Timestamp: number;
  layer2Timestamp: number;
};

export type WeatherForecastSample = {
  sessionType: string;
  timeOffset: number;
  weather: string;
  trackTemperature: number;
  trackTemperatureChange: string;
  airTemperature: number;
  airTemperatureChange: string;
  rainPercentage: number;
};

export type PacketSessionData = {
  header: PacketHeader;

  weather: string;
  trackTemperature: number;
  airTemperature: number;
  totalLaps: number;
  sessionType: string;
  trackId: string;
  sessionTimeLeft: number;
  sessionDuration: number;
  safetyCarStatus: string;
  numWeatherForecastSamples: number;
  weatherForecastSamples: WeatherForecastSample[];

  pitStopWindowIdealLap: number;
  pitStopRejoinPosition: number;

  layer1Timestamp: number;
  layer2Timestamp: number;
};

export type CarLapData = {
  lastLapTimeInMS: number;
  currentLapTimeInMS: number;
  sector1TimeInMS: number;
  sector2TimeInMS: number;
  deltaToCarInFrontInMS: number;
  deltaToRaceLeaderInMS: number;
  safetCarDelta: number;
  carPosition: number;
  currentLapNum: number;
  pitStatus: string;
  numPitStops: number;
  sector: string;
  currentLapInvalid: string;
  penalties: number;
  totalWarnings: number;
  cornerCuttingWarnings: number;
  numUnservedDriveThroughPens: number;
  numUnservedStopGoPens: number;
  gridPosition: number;
  resultStatus: string;
  pitLaneTimeInLaneInMS: number;
  pitStopTimerInMS: number;
  pitStopShouldServePen: string;
};

export type PacketLapData = {
  header: PacketHeader;
  cars: CarLapData[];
  timeTrialPBCarIdx: number;
  layer1Timestamp: number;
  layer2Timestamp: number;
};

export type BaseEvent = {
  type: string;
};

type SessionStartedEvent = BaseEvent & {
  type: "Session Started";
  payload: { data: true };
};

type SessionEndedEvent = BaseEvent & {
  type: "Session Ended";
  payload: { data: true };
};

type FastestLapEvent = BaseEvent & {
  type: "Fastest Lap";
  payload: {
    vehicleIdx: number;
    lapTime: number;
  };
};

type RetirementEvent = BaseEvent & {
  type: "Retirement";
  payload: {
    vehicleIdx: number;
  };
};

type DRSEvent = BaseEvent & {
  type: "DRS Enabled" | "DRS Disabled";
  payload: { data: true };
};

type TeamMateInPitsEvent = BaseEvent & {
  type: "Team Mate In Pits";
  payload: {
    vehicleIdx: number;
  };
};

type ChequeredFlagEvent = BaseEvent & {
  type: "Chequered Flag";
  payload: { data: true };
};

type RaceWinnerEvent = BaseEvent & {
  type: "Race Winner";
  payload: {
    vehicleIdx: number;
  };
};

type PenaltyIssuedEvent = BaseEvent & {
  type: "Penalty Issued";
  payload: {
    penaltyType: string;
    infringementType: string;
    vehicleIdx: number;
    otherVehicleIdx: number;
    timeGained: number;
    lapNum: number;
    placesGained: number;
  };
};

type SpeedTrapTriggeredEvent = BaseEvent & {
  type: "Speed Trap Triggered";
  payload: {
    vehicleIdx: number;
    speed: number;
    isOverallFastestInSession: boolean;
    isDriverFastestInSession: boolean;
    fastestVehicleIdxInSession: number;
    fastestSpeedInSession: number;
  };
};

type StartLightEvent = BaseEvent & {
  type: "Start Lights";
  payload: {
    numLights: number;
  };
};

type LightsOutEvent = BaseEvent & {
  type: "Lights Out";
  payload: { data: true };
};

type DriveThroughServedEvent = BaseEvent & {
  type: "Drive Through Served";
  payload: {
    vehicleIdx: number;
  };
};

type StopGoServedEvent = BaseEvent & {
  type: "Stop Go Served";
  payload: {
    vehicleIdx: number;
  };
};

type FlashbackEvent = BaseEvent & {
  type: "Flashback";
  payload: {
    flashbackFrameIdentifier: number;
    flashbackSessionTime: number;
  };
};

type ButtonStatusEvent = BaseEvent & {
  type: "Button Status";
  payload: {
    button: string;
  };
};

type RedFlagEvent = BaseEvent & {
  type: "Red Flag";
  payload: { data: true };
};

type OvertakeEvent = BaseEvent & {
  type: "Overtake";
  payload: {
    overtakingVehicleIdx: number;
    beingOvertakenVehicleIdx: number;
  };
};

type UnknownEvent = BaseEvent & {
  type: "Unknown";
  payload: {
    Unknown: string;
  };
};

export type PacketEventData =
  | SessionStartedEvent
  | SessionEndedEvent
  | FastestLapEvent
  | RetirementEvent
  | DRSEvent
  | TeamMateInPitsEvent
  | ChequeredFlagEvent
  | RaceWinnerEvent
  | PenaltyIssuedEvent
  | SpeedTrapTriggeredEvent
  | StartLightEvent
  | LightsOutEvent
  | DriveThroughServedEvent
  | StopGoServedEvent
  | FlashbackEvent
  | ButtonStatusEvent
  | RedFlagEvent
  | OvertakeEvent
  | UnknownEvent;

export type EventPacket = {
  header: PacketHeader;
  type: PacketEventData["type"];
  payload: PacketEventData["payload"];
  layer1Timestamp: number;
  layer2Timestamp: number;
};

export type BaseParticipant = {
  teamId: string;
  carRaceNumber: number;
  nationality: string;
};

export type HumanParticipant = BaseParticipant & {
  driverName: string;
  networkId: number;
};

export type AIParticipant = BaseParticipant & {
  driverName: string;
};

export type Participant = HumanParticipant | AIParticipant;

export type ParticipantsPacket = {
  header: PacketHeader;
  numActiveCars: number;
  participants: Participant[];
  layer1Timestamp: number;
  layer2Timestamp: number;
};

export type CarTelemetry = {
  speed: number;
  throttle: number;
  steer: number;
  brake: number;
  clutch: number;
  gear: number;
  engineRPM: number;
  drs: number;
  revLightsPercent: number;
  revLightsBitValue: number;
  brakesTemperature: number[];
  tyresSurfaceTemperature: number[];
  tyresInnerTemperature: number[];
  engineTemperature: number;
  tyresPressure: number[];
  surfaceType: string[];
};

export type CarTelemetryPacket = {
  header: PacketHeader;
  suggestedGear: number;
  cars: CarTelemetry[];
  layer1Timestamp: number;
  layer2Timestamp: number;
};

export type CarStatus = {
  frontBrakeBias: number;
  pitLimiterStatus: string;
  fuelRemainingLaps: number;
  drsAllowed: string;
  drsActivationDistance: number;
  actualTyreCompound: string;
  visualTyreCompund: string;
  tyresAgeLaps: number;
  vehicleFiaFlags: string;
  ersStoreEnergy: number;
  ersDeployMode: string;
  ersHarvestedThisLapMguk: number;
  ersHarvestedThisLapMguh: number;
  networkPaused: string;
};

export type CarStatusPacket = {
  header: PacketHeader;
  cars: CarStatus[];
  layer1Timestamp: number;
  layer2Timestamp: number;
};

type WheelsDamage = [number, number, number, number];

export interface CarDamage {
  tyresWear: WheelsDamage;
  tyresDamage: WheelsDamage;
  brakesDamage: WheelsDamage;
  frontLeftWingDamage: number;
  frontRightWingDamage: number;
  rearWingDamage: number;
  floorDamage: number;
  diffuserDamage: number;
  sidepodDamage: number;
  drsFault: number;
  ersFault: number;
  gearBoxDamage: number;
  engineDamage: number;
  engineMguhWear: number;
  engineEsWear: number;
  engineCeWear: number;
  engineIceWear: number;
  engineMgukWear: number;
  engineTcWear: number;
  engineBlown: number;
  engineSeized: number;
}

export interface PacketCarDamageDataJSON {
  header: PacketHeader;
  cars: CarDamage[];
}

export interface LapHistoryDataJSON {
  lapTimeInMS: number;
  sector1TimeInMS: number;
  sector2TimeInMS: number;
  sector3TimeInMS: number;
  lapValidBitFlags: string;
}

export interface TyreStintHistoryDataJSON {
  endLap: number;
  tyreActualCompound: string;
  tyreVisualCompound: string;
}

export interface PacketSessionHistoryDataJSON {
  header: PacketHeader;
  carIdx: number;
  numLaps: number;
  numTyreStints: number;
  bestLapTimeLapNum: number;
  bestSector1LapNum: number;
  bestSector2LapNum: number;
  bestSector3LapNum: number;
  lapHistoryData: LapHistoryDataJSON[];
  tyreStintHistoryData: TyreStintHistoryDataJSON[];
}

export interface TyreSetDataJSON {
  actualTyreCompound: string;
  visualTyreCompound: string;
  wear: number;
  available: number;
  recommendedSession: number;
  lifeSpan: number;
  usableLife: number;
  lapDeltatime: number;
  fitted: number;
}

export interface PacketTyreSetsDataJSON {
  header: PacketHeader;
  carIdx: number;
  fittedIdx: number;
  tyreSets: TyreSetDataJSON[];
}
