//
//  HTTPManager.swift
//  data4help
//
//  Created by Alessandro Nichelini on 12/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import Foundation
import SwiftyJSON
import Alamofire
import HealthKit

class HTTPManager {
    
    static func sendHeartData(data: [HKQuantitySample])  {
        let credential = URLCredential(user: "user", password: "pass", persistence: .forSession)
        var toSend : JSON = [:]
        var heartJson : JSON
        
        var bpm, timestamp, roundKey : String
        var i = 0
        
        for hkqs in data {
            bpm = "\(hkqs.quantity)"
            timestamp = "\(hkqs.startDate)"
            heartJson =  ["bpm": bpm, "timestamp": timestamp]
            
            roundKey = "data" + String(i)
            do { try toSend.merge(with: [roundKey : heartJson]) }
            catch {}
            i = i + 1
        }
        let parameters : Parameters = toSend.dictionaryObject ?? [:]
        let url = Global.getUserURL() + Global.HEART_ENDPOINT
        Alamofire.request(url, method: .post, parameters: parameters, encoding: JSONEncoding.default)
            .authenticate(usingCredential: credential)
    }
}
