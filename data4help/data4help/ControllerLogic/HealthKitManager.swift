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
    
    public static func checkIfHealtkitIsEnabled (_ notAuthNotificationHandler: @escaping ((Bool) -> ())) {
        var authStatus = healthKitStore.authorizationStatus(for: HKObjectType.quantityType(forIdentifier: .heartRate)!)
        if authStatus == HKAuthorizationStatus.notDetermined || authStatus == HKAuthorizationStatus.sharingDenied {
            notAuthNotificationHandler(false)
        } else { notAuthNotificationHandler(true)}
    }
    
    static func getLastHeartBeat () -> [HKQuantitySample] {
        let lastUpdateDate = UserDefaults.standard.object(forKey: "timestampOfLastDataRetrieved")
        
        let myEndDate = Date()
        let myStartDate : Date
        if lastUpdateDate == nil {
            myStartDate = myEndDate.addingTimeInterval(-60*60*24)
        } else {
            myStartDate = (lastUpdateDate as! Date).addingTimeInterval(1)
        }
        
        let timeIntervalPredicate =
            HKQuery.predicateForSamples(withStart: myStartDate,
                                        end: myEndDate, options: [])
        
        let sampleType = HKSampleType.quantityType(forIdentifier: HKQuantityTypeIdentifier.heartRate)
        
        var semaphore = 0
        
        var samples = [HKQuantitySample]()
        let descriptor = NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: true)
        let query = HKSampleQuery(sampleType: sampleType!, predicate: timeIntervalPredicate, limit: Int(HKObjectQueryNoLimit), sortDescriptors: [descriptor]) {
            query, results, error in
            //Controlla se è stata data l'autorizzazione!!!
            samples = results as! [HKQuantitySample]
            semaphore = 1
        }
        healthStore.execute(query)
        while semaphore == 0 {
            sleep(1)
        }
        
        // If I0ve found some elements, I save the date of the last of them in order to have a reference of the timestamp of the last retrieved sample
        if samples.count != 0 {
            let lastTimestamp = samples[samples.count - 1].startDate
            UserDefaults.standard.set(lastTimestamp, forKey: "timestampOfLastDataRetrieved")
        }
        return samples
    }
}
