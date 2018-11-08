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
	subject: User,
	status: RequestStatus
}

sig Data {
	location: Location,
	bpm: Int
} { bpm > 0}

sig SOS {
	triggeredBy: Data,
	vital: Int
} { vital > 0}

-- All user's not fondamental fields are omitted.
-- Identification pass trough a single integer field "Id"
sig User {
	id: Int,
	data: set Data
}{ id > 0 }

sig ThirdParty {
	id: Int,
	subscribedUsers: set User,
	requests: set Request
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
	no disjoint u1, u2 : User | u1.id = u2.id 
	no disjoint t1,t2: ThirdParty | t1.id = t2.id 
	no disjoint d1,d2 : Date | d1.day = d2.day 
	no disjoint r1,r2 : Request | some t: ThirdParty | 
		r1 in t.requests and r2 in  t.requests and
		r1.subject = r2.subject
	no disjoint s1,s2 : SOS | s1.triggeredBy = s2.triggeredBy
	
}
-- Paths exist only if associated with one running event.
-- Date exist only if associated with one running event.
-- Since data are collected by the user, they cannot exist without him/her
-- Requests only exist if the associated Third Party exist
fact existence {
	all p : Path | one r: RunningEvent | r.path = p 
	all d: Date | one r: RunningEvent | r.date = d 
	all d: Data | one u: User | d in u.data
	all r: Request | one t: ThirdParty | r in t.requests 
	all r: Request | one u: User | r.subject = u
}

fact subscriptions {	
	--all t: ThirdParty, u: User | some r: Request | 
	-- if there is a request from a third party to a user that is APPROVED, then that third party is 
	-- subscribed to that user
	all r:  Request, t: ThirdParty | 
		(r in t.requests and r.status = APPROVED)
			implies
		r.subject in t.subscribedUsers

	-- if there is a request from a third party to a user that is DECLINED or PENDING, that third party
	-- cannot be subscribed to that user
	all r:  Request, t: ThirdParty | 
		(r in t.requests and (r.status = DECLINED or r.status = PENDING))
			implies
		r.subject not in t.subscribedUsers
	
	-- if there is a third party which is subscribed to a user, then there must be a request approved 
	-- for that third party and for that user
	all t: ThirdParty, u: User | 
		u in t.subscribedUsers 
			implies 
		some r: Request | r.status = APPROVED and r.subject = u and r in t.requests
}

-- 
fact SOS {
	all s: SOS | s.vital < 4
	all s: SOS | one d: Data | s.vital = d.bpm and s.triggeredBy = d
}

/*** PREDICATES ***/
pred makeARequest [t: ThirdParty, u: User, r: Request]{
	r.subject = u
	r.status = PENDING
	t.requests = t.requests + r
}

pred approveARequest [t, t':ThirdParty, u:User, r, r' :Request] {
	r'.subject = r.subject
	r'.status = APPROVED
	t'.requests  = t.requests + r'
	t'.subscribedUsers = t.subscribedUsers + u
}

pred show {
	#User > 2
	#ThirdParty > 1
	#SOS > 2
	#Location > 1
	#RunningEvent >1
	
	all u: User | #u.data > 0
	all t: ThirdParty | #t.requests > 0
	some r: Request | r.status = APPROVED
	some r: Request | r.status = DECLINED
}

--run makeARequest
run approveARequest for 5 but 8 Int
--run show
