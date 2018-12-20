//
//  LocationManager.swift
//  data4help
//
//  Created by Francesco Peressini on 20/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import Foundation
import CoreLocation

class LocationManager {
    
    public static func checkIfLocationIsEnabled (_ notAuthNotificationHandler: @escaping ((Bool) -> ())) {
        if CLLocationManager.locationServicesEnabled() {
            switch CLLocationManager.authorizationStatus() {
            case .notDetermined, .restricted, .denied:
                notAuthNotificationHandler(false)
            case .authorizedAlways, .authorizedWhenInUse:
                notAuthNotificationHandler(true)
            }
        }
        else {
            notAuthNotificationHandler(false)
        }
    }
    
}
