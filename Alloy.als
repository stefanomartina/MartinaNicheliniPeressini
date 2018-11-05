abstract sig EventStatus  {}
one sig LIVE extends EventStatus {}
one sig SCHEDULED extends EventStatus{}
one sig FINISHED extends EventStatus{}
one sig CANCELLED extends EventStatus{}

sig RunningEvent {
	runners: set User,
	path: one Path,
	date: Date
}

abstract sig RequestStatus{}
one sig APPROVED extends RequestStatus{}
one sig DECLINED extends RequestStatus{}
one sig PENDING extends RequestStatus{}

sig Request {
	sender: ThirdParty,
	subject: User,
	status: RequestStatus
}

sig Data {
	location: Location,
	bpm: Int
} { bpm > 0}

-- All user' not foundamental fields are omitted.
-- Identification pass trough a single int filed "Id"
sig User {
	id: Int,
	data: set Data
}{ id > 0 }

sig ThirdParty {
	id: Int,
	subscribedUsers: set User
}{ id > 0}

-- In this Alloy model, date are simplified and represented with a single number.
sig Date {
	day: Int
}{ day > 0 }

sig Location {
	coordinateX: Int,
	coordinateY: Int
} { coordinateX > 0 and coordinateY >0 }


sig Path {
	startingLocation: one Location,
	endingLocation: one Location
}


/*** FACTS ***/
fact uniqueEntities {
	no disjoint u1, u2 : User | u1.id = u2.id and
	no disjoint t1,t2: ThirdParty | t1.id = t2.id and
	no disjoint d1, d2 : Date | d1.day = d2.day
}
-- Paths exist only if associated with one running event.
-- Date exist only if associated with one running event.
-- Since data are collected by the user, they cannot exist witouth him/her
fact onlyRunningPath {
	all p : Path | one r: RunningEvent | r.path = p and
	all d: Date | one r: RunningEvent | r.date = d and
	all d: Data | one u: User | d in u.data
}
-- Requests only exist if the associated Third Party exist
fact requestExistence {
	all r: Request | one t: ThirdParty | r.sender = t and
	all r: Request | one u: User | r.subject = u
}

fact subscriptions {
	
	-- if there is a request from a third party to a user that is DECLINED or PENDING, that third party
	-- cannot be subscribed to that user
	all r: Request, t: ThirdParty | 
		r.sender = t and (r.status = DECLINED or r.status = PENDING)
			implies
		r.subject not in t.subscribedUsers
	
	-- if there is a request from a third party to a user that is APPROVED, then that third party is 
	-- subscribed to that user
	all r: Request, t: ThirdParty | 
		r.sender = t and r.status = APPROVED
			implies
		r.subject in t.subscribedUsers
	
	-- if there is a third party which is subscribed to a user, then there must be a request approved 
	-- for that third party and for that user
	all t: ThirdParty, u: User | some r: Request | 
		u in t.subscribedUsers 
			implies
		r.subject = u and r.sender = t and r.status = APPROVED	
}




pred show {
}

run show
