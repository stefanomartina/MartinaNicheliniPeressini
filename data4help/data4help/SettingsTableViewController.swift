//
//  SettingsTableViewController.swift
//  data4help
//
//  Created by Francesco Peressini on 01/01/2019.
//  Copyright © 2019 Francesco Peressini. All rights reserved.
//

import UIKit
import HealthKit
import Foundation

class SettingsTableViewController: UITableViewController {
    
    @IBOutlet weak var healthToggle: UISwitch!
    @IBOutlet weak var emergencyToggle: UISwitch!
    @IBOutlet weak var thresholdLabel: UILabel!
    @IBOutlet weak var thresholdSlider: UISlider!
    @IBOutlet weak var submitThreshold: UIButton!
    @IBOutlet weak var restoreUserDefaultsButton: UIButton!
    
    @IBAction func healthAccess(_ sender: Any) {
        if let senderSwitch = sender as? UISwitch {
            if senderSwitch.isOn {
                let permissionsNedeed = Set([HKObjectType.quantityType(forIdentifier: .heartRate)!])
                HealthKitManager.getHealthStore().requestAuthorization(toShare: permissionsNedeed, read: permissionsNedeed) { (success, error) in if !success { print("errore") } }
            }
        }
    }
    
    @IBAction func emergencyService(_ sender: Any) {
        if(emergencyToggle.isOn ){ Global.userDefaults.set(true, forKey: "automatedSOSToggle") }
        else { Global.userDefaults.set(false, forKey: "automatedSOSToggle") }
    }
    
    // For debug purpose
    @IBAction func restoreUserDefaults(_ sender: Any) {
        UserDefaults.standard.set(nil, forKey: "timestampOfLastDataRetrieved")
    }
    
    
    ////////////////////////////////////// AUTOMATED SOS TOGGLE STATUS RETRIEVAL
    func setAutomatedSOSSwitch(){
        let status = Global.userDefaults.bool(forKey: "automatedSOSToggle")
        healthToggle.setOn(status, animated: true)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.allowsSelection = false;
        setAutomatedSOSSwitch()
        thresholdLabel.text = getThreshold()
        setSlider()
        
        HealthKitManager.checkIfHealtkitIsEnabled({ response in
            self.healthToggle.setOn(response, animated: true)
            self.healthToggle.isEnabled = !response
        })
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        
        setSlider()
    }
    
    ////////////////////////////////////// SLIDER SETUP and ASSOCIATED FUNCTIONS
    func setSlider(){
        submitThreshold.isEnabled = false
        thresholdSlider.minimumValue = 20
        thresholdSlider.maximumValue = 100
        thresholdSlider.isContinuous = true
        thresholdSlider.setValue(Float(getThreshold())!, animated: true)
    }
    
    func getThreshold() -> String{
        if let tok = Global.userDefaults.string(forKey: "threshold") {
            print(tok)
            return tok
        } else {
            print(String(Global.DEFAULT_THRESHOLD))
            return String(Global.DEFAULT_THRESHOLD)
        }
    }
    @IBAction func thresholdSliderChanges(_ sender: Any) {
        let tok = String("\(thresholdSlider.value)").components(separatedBy: ".")[0]
        thresholdLabel.text = "\(tok)"
        if(Int(getThreshold()) != Int(tok)){
            submitThreshold.isEnabled = true;
        }
        else{
            submitThreshold.isEnabled = false;
        }
    }
    
    @IBAction func submitCustomThreshold(_ sender: Any) {
        let tok = String("\(thresholdSlider.value)").components(separatedBy: ".")[0]
        Global.userDefaults.set(tok, forKey: "threshold")
        submitThreshold.isEnabled = false;
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return 3
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        if section == 1 {
            return 2
        }
        else {
            return 1
        }
    }

}
