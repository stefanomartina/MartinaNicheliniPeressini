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
        var toSend : JSON
        var heartJson : JSON
        
        var bpm : String
        var timestamp : String
        
        var roundKey : String
        var i = 0
        
        for hkqs in data {
            bpm = "\(hkqs.quantity)"
            timestamp = "\(hkqs.startDate)"
            heartJson =  ["bpm": bpm, "timestamp": timestamp]
    
//            toSend.merge(with: [""])
        }
    }
    
}
