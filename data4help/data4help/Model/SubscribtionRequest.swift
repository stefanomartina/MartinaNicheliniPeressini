//
//  SubscribtionRequest.swift
//  data4help
//
//  Created by Alessandro Nichelini on 19/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import Foundation

enum subscriptionStatus: String {
    case approved
    case rejected
    case pending
    case UNDEFINED
}

struct subscribtionRequest {
    var status = subscriptionStatus.UNDEFINED
    var requesterName = String()
    var description = String()
}
