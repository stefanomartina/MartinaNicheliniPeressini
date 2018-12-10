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



class Global {
    
    static private var USER_URL = ""
    static private let URL_USER_LOCAL = "http://localhost:5000/api/users"
    static private let URL_USER_REMOTE = "http://data4help.cloud:5000/api/users"
    static public let LOGIN_METHOD = "/login"
    
    static public func getUserURL(_ completionHandler: (() -> Void)? = nil)  -> String {
        if USER_URL == "" {
            //When global class is initialiazed, the right URL is chosen
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
                    completionHandler!()
            }
        }
        return USER_URL
    }

}
