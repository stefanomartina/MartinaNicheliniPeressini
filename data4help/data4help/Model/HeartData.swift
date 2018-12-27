//
//  HeartData.swift
//  data4help
//
//  Created by Alessandro Nichelini on 22/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import Foundation
import SwiftyJSON
import HealthKit

class Data {
    var timestamp: String = ""
    
    init (data: Date){
        self.timestamp = "   "+"\(data)"
    }
    
    init (data: String){
        self.timestamp = data
    }
}

class HeartData : Data {
    var bpm : String
    
    init(data: HKQuantitySample) {
        let tmp = "\(data.quantity)"
        self.bpm = String(tmp.split(separator: " ")[0])
        super.init(data: data.startDate)
    }
    
    init(data: JSON){
        self.bpm = data["bpm"].stringValue
        super.init(data: data["timestamp"].stringValue)
    }
}

class LocationData : Data {
    var latitude: Double = 0.0
    var longitude: Double = 0.0
    
    init(data: JSON){
        self.latitude = Double(data["Latitude"].stringValue)!
        self.longitude = Double(data["Longitude"].stringValue)!
        super.init(data: "   "+data["timestamp"].stringValue)
    }
}
