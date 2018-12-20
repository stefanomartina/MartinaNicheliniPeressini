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
    
    var locationManager: CLLocationManager!

    @IBOutlet weak var healthToggleSwitch: UISwitch!
    @IBOutlet weak var locationToggleSwitch: UISwitch!
    
    // HEALTH TOGGLE
    @IBAction func switchToggled(_ sender: Any) {
        if let senderSwitch = sender as? UISwitch {
            if senderSwitch.isOn {
                let permissionsNedeed = Set([HKObjectType.quantityType(forIdentifier: .heartRate)!])
                    HealthKitManager.getHealthStore().requestAuthorization(toShare: permissionsNedeed, read: permissionsNedeed) { (success, error) in if !success { print("errore") } }
            }
        }
    }
    
    // LOCATION TOGGLE
    @IBAction func locationToggle(_ sender: Any) {
        if let senderSwitch = sender as? UISwitch {
            if senderSwitch.isOn {
                if CLLocationManager.locationServicesEnabled() {
                    locationManager = CLLocationManager()
                    locationManager.delegate = self
                    locationManager.requestAlwaysAuthorization()
                }
                else {
                    let alert = UIAlertController(title: "Attention!", message: "Location services not enabled", preferredStyle: .alert)
                    alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
                    self.present(alert, animated: true)
                }
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        HealthKitManager.checkIfHealtkitIsEnabled({ response in
            self.healthToggleSwitch.setOn(response, animated: true)
            self.healthToggleSwitch.isEnabled = !response
            })
        LocationManager.checkIfLocationIsEnabled({ response in
            self.locationToggleSwitch.setOn(response, animated: true)
            self.healthToggleSwitch.isEnabled = !response
        })
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
    }

}
