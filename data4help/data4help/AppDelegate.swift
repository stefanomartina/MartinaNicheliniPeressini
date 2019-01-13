//
//  AppDelegate.swift
//  data4help
//
//  Created by Francesco Peressini on 28/11/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit
import UserNotifications

////////////////////////////////////////////// DECLARATION OF NOTIFCATION DELEGATE AND NOTIFICATION CENTER
let notificationDelegate = NotificationCenter()
let center = UNUserNotificationCenter.current()
var sosTimer : Timer!

// all actions to be settuped app in the App delegates but activated only once user logged in 
func loginServicesActivation() {
    center.delegate = notificationDelegate
    HealthKitManager.activateLongRunningQuery()
}

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        //Global.userDefaults.set(60, forKey: "threshold")  // debug purpose
        
        ////////////////////////////////////////////// NOTIFICATION PERMISSION
        let options: UNAuthorizationOptions = [.alert, .sound];
        //center.delegate = notificationDelegate  ----> better to assign it when user logs in. Implemented in loginServicesActivation functions
        center.requestAuthorization(options: options) {
            (granted, error) in if !granted { print("Something went wrong") } }
        NotificationCenter.defineCustomNotificationActions()
        
        //////////////////////////////////////////////  HEALTHKIT LONG QUERY ACTIVATION
        //HealthKitManager.activateLongRunningQuery() ----> better to assign it when user logs in. Implemented in loginServicesActivation functions
        
        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }

}

