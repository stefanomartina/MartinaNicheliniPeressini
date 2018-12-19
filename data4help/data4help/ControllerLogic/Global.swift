//
//  Global.swift
//  data4help
//
//  Created by Alessandro Nichelini on 10/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//
//
import Foundation
import Alamofire


//Let's put all global variable in this class. All methods and varibles have to be statis
class Global {
    static private var USER_URL = ""
    static private let URL_USER_LOCAL = "http://localhost:5000/api/users"
    static private let URL_USER_REMOTE = "http://data4help.cloud:5000/api/users"
    
    static public let LOGIN_METHOD = "/login"
    static public let REGISTER_METHOD = "/register"
    static public let HEART_ENDPOINT = "/data/heart"
    static public let HEART_ENDPOINT_GET = "/data/heart/get_data"
    static public let SUBSCRIPTION = "/subscription"
    
    //This method handles the selection of the right URL.
    static public func getUserURL(_ completionHandler: (() -> Void)? = nil)  -> String {
        if USER_URL == "" {
            Alamofire.request(URL_USER_LOCAL)
                .validate()
                .responseJSON { response in
                    switch response.result {
                    case .success:
                        print("Validation Successful")
                        self.USER_URL = URL_USER_LOCAL
                    case .failure:
                        print("Errors")
                        self.USER_URL = URL_USER_REMOTE
                    }
                    completionHandler?()
            }
        }
        return USER_URL
    }

}

//Let's put all messages here instead of inserting them directly in code snippets.
class Messages {
    static public let LOGIN_ERROR = "Login error: server didn't response"
}

