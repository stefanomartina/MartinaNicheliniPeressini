//
//  NotificationCenter.swift
//  data4help
//
//  Created by Alessandro Nichelini on 28/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import Foundation
import UserNotifications

class NotificationCenter : NSObject, UNUserNotificationCenterDelegate {
    
    // function to register custom notification actions
    static func defineCustomNotificationActions() {
        let okAction = UNNotificationAction(identifier: Global.SOSOkActionID,
                                                title: "I'm OK", options: [])
        
        let category = UNNotificationCategory(identifier: Global.SOSCategoryID,
                                              actions: [okAction],
                                              intentIdentifiers: [], options: [])
        
        center.setNotificationCategories([category])
    }
    
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                willPresent notification: UNNotification,
                                withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        // Play sound and show alert to the user
        completionHandler([.alert,.sound])
    }
    
    
    ///////////////////////////////////////// NOTIFICATION CENTER AS A DELEGATOR: define here notification action callback
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                didReceive response: UNNotificationResponse,
                                withCompletionHandler completionHandler: @escaping () -> Void) {
        // Determine the user action
        switch response.actionIdentifier {
        case Global.SOSOkActionID:
            print ("It'all ok")
        default:
            print("Unknown action")
        }
        completionHandler()
    }
}
