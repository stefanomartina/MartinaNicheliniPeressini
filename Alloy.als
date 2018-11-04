open util/time
open util/boolean

sig Location {
	coordinateX: one Int,
	coordinateY: one Int
}

sig Path {
	mapURL: one String,
	startingLocation: one Location,
	endingLocation: one Location
}

abstract sig EventStatus  {}
one sig LIVE extends EventStatus {}
one sig SCHEDULED extends EventStatus{}
one sig FINISHED extends EventStatus{}
one sig CANCELLED extends EventStatus{}

sig RunningEvent {
	name: one String,
	location: one Location,
	date: one Time,
	status: one EventStatus,
	partecipants: set User,
	lenght: one Int,
	path: one Path
}

sig User {
	username: one String,
	passwords: one String,
	fiscalCode: one String,
	hometown: one String,
	elderly: one Bool, 
	runner: one Bool,
	activeEvents: set RunningEvent,
	spectatorEvents: set RunningEvent
}

sig ThirdParty {
	name: one String,
	id: one String,
	trusted: one Bool
}

abstract sig Data {
	generatedBy: User,
	timestamp: Time
}
sig LocationData extends Data {
	location: Location,
	motionStatus: Bool
}
sig HealthData extends Data {
	vital: Bool
}

-- Usernames are unique
fact uniqueUsername {
	no disjoint u1, u2: User | u1.username = u2.username
}

-- IDs are unique
fact uniqueIDs {
	no disjoint t1,t2: ThirdParty | t1.id = t2.id
}

-- a user cannot be involved in two simultaneous events as a runner.
fact noSimultaneousEvents {
	all user: User | no disjoint e1, e2: RunningEvent |
		e1 in user.activeEvents and e2 in user.activeEvents and
		e1.status = LIVE and e2.status = LIVE
}
