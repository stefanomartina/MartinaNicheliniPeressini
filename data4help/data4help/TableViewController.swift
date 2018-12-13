//
//  TableViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 12/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit
import HealthKit
import Alamofire

struct Data{
    var opened = Bool()
    var title = String()
    var sectionData = [String()]
}

class TableViewController: UITableViewController {
    var sem = false
    var tableViewData = [Data]()
    
    @IBAction func updateAndUpload(_ sender: Any) {
        updateDataFromHealtKit()
        print("Sono dentro qui")
    }
    
    func updateDataFromHealtKit(){
        let queryReturned: [HKQuantitySample] = HealthKitManager.getLastHeartBeat()
        var bpm, timestamp : String
        
        if queryReturned.count == 0 {
            let message = "No new data were found"
            let alert = UIAlertController(title: "Attention", message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
            self.present(alert, animated: true)
        }
        else {
            let message = String(format: "%x%@", queryReturned.count, " elements were found")
            let alert = UIAlertController(title: "Success", message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
            self.present(alert, animated: true)
            
            for hkqs in queryReturned {
                bpm = "\(hkqs.quantity)"
                timestamp = "\(hkqs.startDate)"
                
                tableViewData += [Data(opened: false, title: bpm, sectionData: [timestamp])]
            }
            self.tableView.reloadData()
        }
        DispatchQueue.main.async {
            HTTPManager.sendHeartData(data: queryReturned)
        }
    }
    
    func updateDataFromDB(){
        let URL_USER_REGISTER = Global.getUserURL() + Global.HEART_ENDPOINT_GET
        
        
        Alamofire.request(URL_USER_REGISTER, method: .post, encoding: JSONEncoding.default)
            .responseJSON {
                response in
                if let status = response.result.value {
                    let JSON = status as! NSDictionary;
                    let appo = JSON["Response"]!;
                    print(appo)
                }
        }
    }
    
    override func viewDidLoad() {
        //così se vogliamo ogni volta che carichiamo il tab vengono ribeccati i dati
        //direi comunque che i dati da displayare (fino a che non viene piagiato sul refresh) siano quelli del db ---> ROBA che mi manda fra e poi implemento

        updateDataFromHealtKit()
        
        
        updateDataFromDB()
        
        
        
        super.viewDidLoad()
        print("entrato")
    }
    
    override func numberOfSections(in tableView: UITableView) -> Int {
        return tableViewData.count
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if tableViewData[section].opened == true{
            return tableViewData[section].sectionData.count + 1
        }else{
            return 1
        }
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let dataIndex = indexPath.row - 1
        if indexPath.row == 0{
            guard let cell = tableView.dequeueReusableCell(withIdentifier: "cell") else { return UITableViewCell() }
            cell.textLabel?.text = tableViewData[indexPath.section].title
            return cell
        }else{
            guard let cell = tableView.dequeueReusableCell(withIdentifier: "cell") else { return UITableViewCell() }
            cell.textLabel?.text = tableViewData[indexPath.section].sectionData[dataIndex]
            return cell
        }
    }
    
    
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        if tableViewData[indexPath.section].opened == true{
            tableViewData[indexPath.section].opened = false
            let sections = IndexSet.init(integer: indexPath.section)
            tableView.reloadSections(sections, with: .none)
        }else{
            tableViewData[indexPath.section].opened = true
            let sections = IndexSet.init(integer: indexPath.section)
            tableView.reloadSections(sections, with: .none)
        }
    }
}
