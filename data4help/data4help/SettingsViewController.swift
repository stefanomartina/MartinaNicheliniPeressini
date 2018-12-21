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
import Foundation

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
    
    @IBOutlet weak var labelThreshold: UILabel!
    @IBOutlet weak var sliderThreshold: UISlider!
    @IBOutlet weak var submitCustomThresholdButton: UIButton!
    @IBOutlet weak var automatedSOSToggle: UISwitch!
    
    @IBAction func automatedSOSSwitch(_ sender: Any) {
        if( automatedSOSToggle.isOn ){
            Global.userDefaults.set(true, forKey: "automatedSOSToggle")
        }else{
            Global.userDefaults.set(false, forKey: "automatedSOSToggle")
        }
        
    }
    @IBAction func sliderThresholdChanges(_ sender: Any) {
        let tok = String("\(sliderThreshold.value)").components(separatedBy: ".")[0]
        labelThreshold.text = "\(tok)"
        if(Int(getThreshold()) != Int(tok)){
            submitCustomThresholdButton.isEnabled = true;
        }
        else{
            submitCustomThresholdButton.isEnabled = false;
        }
    }
    
    @IBAction func submitThresholdCHanges(_ sender: Any) {
        let tok = String("\(sliderThreshold.value)").components(separatedBy: ".")[0]
        Global.userDefaults.set(tok, forKey: "threshold")
        submitCustomThresholdButton.isEnabled = false;
    }
    
    func getThreshold() -> String{
        return Global.userDefaults.string(forKey: "threshold") ?? String(Global.DEFAULT_THRESHOLD)
    }
    
    func setSlider(){
        submitCustomThresholdButton.isEnabled = false
        sliderThreshold.minimumValue = 20
        sliderThreshold.maximumValue = 100
        sliderThreshold.isContinuous = true
        sliderThreshold.setValue(Float(getThreshold())!, animated: true)
    }
    
    func setAutomatedSOSSwitch(){
        let status = Global.userDefaults.bool(forKey: "automatedSOSToggle")
        print(status)
        healthToggleSwitch.setOn(status, animated: true)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        labelThreshold.text = getThreshold()
        setSlider()
        setAutomatedSOSSwitch()
        
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
