//
//  SettingsViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 03/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit
import HealthKit
import CoreLocation

class SettingsViewController: UIViewController, CLLocationManagerDelegate {
    
    @IBOutlet weak var locationToggleSwitch: UISwitch!
    @IBOutlet weak var healthToggleSwitch: UISwitch!

    // HEALTH TOGGLE
    @IBAction func switchToggled(_ sender: Any) {
        if let senderSwitch = sender as? UISwitch {
            if senderSwitch.isOn {
                let permissionsNedeed = Set ([HKObjectType.quantityType(forIdentifier: .heartRate)!])
                
                    HealthKitManager.getHealthStore().requestAuthorization(toShare: permissionsNedeed, read: permissionsNedeed) { (success, error) in
                    if !success {
                        print("errore")
                    }
                }
            } // end if sender.isOn
        } //end if casting
    }
    
    // LOCATION TOGGLE
    @IBAction func locationToggle(_ sender: Any) {
        if let senderSwitch = sender as? UISwitch {
            if senderSwitch.isOn {
                let locationManager = CLLocationManager()
                locationManager.requestAlwaysAuthorization()
                
                if CLLocationManager.locationServicesEnabled() {
                    locationManager.delegate = self
                    locationManager.desiredAccuracy = kCLLocationAccuracyBest
                    locationManager.startUpdatingLocation()
                }
            }
        }
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        if let location = locations.first {
            print(location.coordinate)
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let healthToggleSwitchStatus = UserDefaults.standard.bool(forKey: "healthToggleStatus")
        let locationToggleStatus = UserDefaults.standard.bool(forKey: "locationToggleStatus")
        healthToggleSwitch.setOn(healthToggleSwitchStatus, animated: true)
        locationToggleSwitch.setOn(locationToggleStatus, animated: true)
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        UserDefaults.standard.set(healthToggleSwitch.isOn, forKey: "healthToggleStatus")
        UserDefaults.standard.set(locationToggleSwitch.isOn, forKey: "locationToggleStatus")
    }

}
