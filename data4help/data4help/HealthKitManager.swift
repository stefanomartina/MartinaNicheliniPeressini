//
//  HealthKitBridge.swift
//  data4help
//
//  Created by Alessandro Nichelini on 12/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import Foundation
import HealthKit

class HealthKitManager {
    
    static private let healthStore = HKHealthStore()
    
    static func getHealthStore() -> HKHealthStore {
        return healthStore
    }
    
    static func getLastHeartBeat () -> [HKQuantitySample] {
        let myEndDate = Date()
        let myStartDate = myEndDate.addingTimeInterval(-60*60*24)
        
        let timeIntervalPredicate =
            HKQuery.predicateForSamples(withStart: myStartDate,
                                        end: myEndDate, options: [])
        
        let sampleType = HKSampleType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)
        
        var semaphore = 0
        
        var samples = [HKQuantitySample]()
        let query = HKSampleQuery(sampleType: sampleType!, predicate: timeIntervalPredicate, limit: 25, sortDescriptors: nil) {
            query, results, error in
            samples = results as! [HKQuantitySample]
            semaphore = 1
        }
        healthStore.execute(query)
        while semaphore == 0 {
            sleep(1)
        }
        return samples
    }
}
