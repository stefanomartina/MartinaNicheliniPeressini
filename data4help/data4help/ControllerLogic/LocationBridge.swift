//
//  LocationBridge.swift
//  data4help
//
//  Created by Alessandro Nichelini on 12/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import Foundation
import CoreLocation

class LocationManager {
    
    private var locationManager: CLLocationManager!
    
    init() {
       locationManager.requestAlwaysAuthorization()
    }
    
}
