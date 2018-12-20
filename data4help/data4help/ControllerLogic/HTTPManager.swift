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

    static private func getCredential() -> URLCredential {
        return URLCredential(user: UserDefaults.standard.string(forKey: "username")!,
                             password: UserDefaults.standard.string(forKey: "password")!,
                             persistence: .forSession)
    }
    
    static func sendHeartData(data: [HKQuantitySample])  {
        let credential = self.getCredential()
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
    
    static func getDataFromDB(_ updateCallback: @escaping ([Data]) -> ()){
        let URL_USER_REGISTER = Global.getUserURL() + Global.HEART_ENDPOINT_GET
        var retrievedData : [Data] = []
        Alamofire.request(URL_USER_REGISTER, method: .get, encoding: JSONEncoding.default)
            .responseJSON{ response in
                switch response.result {
                case .success(let value):
                    let json = JSON(value)
                    for (_, value): (String, JSON) in json {
                        let bpm = value["bpm"].stringValue
                        let timestamp = "   "+value["timestamp"].stringValue
                        let retrieved = Data(opened: false, title: bpm, sectionData: [timestamp])
                        retrievedData += [retrieved]
                    }
                case .failure(let error):
                    print(error)
                }
                updateCallback(retrievedData)
        }
    }
    
    static func getSubscribtion(_ updateCallback: @escaping ([subscribtionRequest]) -> ()){
        let credential = self.getCredential()
        let URL = Global.getUserURL() + Global.SUBSCRIPTION
        
        
        Alamofire.request(URL, method: .get, encoding: JSONEncoding.default)
            .authenticate(usingCredential: credential)
            .responseJSON { response in
                var dataToReturn : [subscribtionRequest] = []
                switch response.result {
                case .success(let value):
                    let json = JSON(value)
                    for (_, value): (String, JSON) in json {
                        let requester = value["Username_ThirdParty"].stringValue
                        let description = value["description"].stringValue
                        let status = subscriptionStatus(rawValue: value["status"].stringValue )
                        let request = subscribtionRequest(status: status ?? subscriptionStatus.UNDEFINED, requesterName: requester, description: description)
                        dataToReturn = dataToReturn + [request]
                    }
                case .failure(let error):
                    print(error)
                }
                updateCallback(dataToReturn)
        }
    } //end getSubscribtion
    
    static func modifySubscriptionStatus (newStatus: subscriptionStatus, thirdPartyID: String, _ notificationCallback: @escaping (Bool) -> ()){
        let credential = self.getCredential()
        let URL = Global.getUserURL() + Global.SUBSCRIPTION
        let parameters = ["new_status": newStatus.rawValue,
                          "thirdparty": thirdPartyID]

        Alamofire.request(URL, method: .put, parameters: parameters, encoding: JSONEncoding.default)
                .authenticate(usingCredential: credential)
                .responseJSON { response in
                    switch response.result {
                        case .success(let value): notificationCallback(true)
                        case .failure(let error): notificationCallback(false)
                    }
        }
    } //end modifySubscriptionStatus
    
} // end class
