//
//  SettingsViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 03/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit
import HealthKit

let healthStore = HKHealthStore() //i have to keep a reference of this. In this it should be global

class SettingsViewController: UIViewController {
    

    @IBAction func switchToggled(_ sender: Any) {
        if let senderSwitch = sender as? UISwitch{
            if senderSwitch.isOn {
                let permissionsNedeed = Set ([HKObjectType.quantityType(forIdentifier: .heartRate)!])
                
                healthStore.requestAuthorization(toShare: permissionsNedeed, read: permissionsNedeed) { (success, error) in
                    if !success {
                        print("errore")
                    }
                }
            } // end if sender.isOn
        } //end if casting
        
    }
    
    
    @IBOutlet weak var healthToggleSwitch: UISwitch!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let healthToggleSwitchStatus = UserDefaults.standard.bool(forKey: "healthToggleStatus")
        healthToggleSwitch.setOn(healthToggleSwitchStatus, animated: true)
        
        // Do any additional setup after loading the view.
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        UserDefaults.standard.set(healthToggleSwitch.isOn, forKey: "healthToggleStatus")
        }

}
