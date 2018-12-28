//
//  SubscribtionRequest.swift
//  data4help
//
//  Created by Alessandro Nichelini on 19/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import Foundation
import SwiftyJSON

enum subscriptionStatus: String {
    case approved
    case rejected
    case pending
    case UNDEFINED
}

class subscribtionRequest {
    var status : subscriptionStatus
    var requesterName =  String()
    var description = String()
    
    init (jsonInitializer: JSON) {
        self.status = subscriptionStatus(rawValue: jsonInitializer["status"].stringValue) ?? subscriptionStatus.UNDEFINED
        self.requesterName = jsonInitializer["Username_ThirdParty"].stringValue
        self.description = jsonInitializer["description"].stringValue
    }
    
    public func approve(successHandler: @escaping (()->()), errorHandler: @escaping (()->())){
        HTTPManager.modifySubscriptionStatus(newStatus: subscriptionStatus.approved,
                                             thirdPartyID: requesterName
            , { response in
                if response {successHandler()}
                else {errorHandler()}
        })
    } //end method approve
    
    public func deny (successHandler: @escaping (()->()), errorHandler: @escaping (()->())){
        HTTPManager.modifySubscriptionStatus(newStatus: subscriptionStatus.rejected,
                                             thirdPartyID: requesterName
            , { response in
                if response {successHandler()}
                else {errorHandler()}
        })
    } //end method deny
    
}
