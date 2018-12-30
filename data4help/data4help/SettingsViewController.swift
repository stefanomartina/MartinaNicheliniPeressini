//
//  SettingsViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 03/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit
import HealthKit
import Foundation

class SettingsViewController: UIViewController {
    
    @IBOutlet weak var healthToggleSwitch: UISwitch!
    
    // HEALTH TOGGLE
    @IBAction func switchToggled(_ sender: Any) {
        if let senderSwitch = sender as? UISwitch {
            if senderSwitch.isOn {
                let permissionsNedeed = Set([HKObjectType.quantityType(forIdentifier: .heartRate)!])
                    HealthKitManager.getHealthStore().requestAuthorization(toShare: permissionsNedeed, read: permissionsNedeed) { (success, error) in if !success { print("errore") } }
            }
        }
    }
    
    @IBOutlet weak var labelThreshold: UILabel!
    @IBOutlet weak var sliderThreshold: UISlider!
    @IBOutlet weak var submitCustomThresholdButton: UIButton!
    @IBOutlet weak var automatedSOSToggle: UISwitch!
    
    @IBAction func automatedSOSSwitch(_ sender: Any) {
        if( automatedSOSToggle.isOn ){ Global.userDefaults.set(true, forKey: "automatedSOSToggle") }
        else { Global.userDefaults.set(false, forKey: "automatedSOSToggle") }
        
    }
    
    
    // For debug purpose
    @IBAction func resetUserDefaults(_ sender: Any) {
      UserDefaults.standard.set(nil, forKey: "timestampOfLastDataRetrieved")
    }
    
    func getThreshold() -> String{
        return Global.userDefaults.string(forKey: "threshold") ?? String(Global.DEFAULT_THRESHOLD)
    }
    
    ////////////////////////////////////// SLIDER SETUP and ASSOCIATED FUNCTIONS
    func setSlider(){
        submitCustomThresholdButton.isEnabled = false
        sliderThreshold.minimumValue = 20
        sliderThreshold.maximumValue = 100
        sliderThreshold.isContinuous = true
        sliderThreshold.setValue(Float(getThreshold())!, animated: true)
    }
    
    @IBAction func submitThresholdCHanges(_ sender: Any) {
        let tok = String("\(sliderThreshold.value)").components(separatedBy: ".")[0]
        Global.userDefaults.set(tok, forKey: "threshold")
        submitCustomThresholdButton.isEnabled = false;
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
    
    ////////////////////////////////////// AUTOMATED SOS TOGGLE STATUS RETRIEVAL
    func setAutomatedSOSSwitch(){
        let status = Global.userDefaults.bool(forKey: "automatedSOSToggle")
        print(status)
        healthToggleSwitch.setOn(status, animated: true)
    }
    
    
    
    ////////////////////////////////////// UIController standards methods
    override func viewDidLoad() {
        super.viewDidLoad()
        labelThreshold.text = getThreshold()
        setSlider()
        setAutomatedSOSSwitch()
        
        HealthKitManager.checkIfHealtkitIsEnabled({ response in
            self.healthToggleSwitch.setOn(response, animated: true)
            self.healthToggleSwitch.isEnabled = !response
            })
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
    }
}
