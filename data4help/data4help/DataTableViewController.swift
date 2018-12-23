//
//  DataTableViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 22/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit
import HealthKit

class DataTableViewController: UITableViewController {
    
    var data = [HeartData]()
    
    ////////////////////////////////////////////////////
    private func fetchData(){
        HTTPManager.getDataFromDB { retrievedData in
            self.data = retrievedData
            self.tableView.reloadData()
        }
    }
    
    private func loadAndSendData(alsoFetch: Bool) {
        let queryReturned: [HKQuantitySample] = HealthKitManager.getLastHeartBeat()
        
        var bpm, timestamp, bpm_str : String
        
        if queryReturned.count != 0 {
            for hkqs in queryReturned {
                bpm = "\(hkqs.quantity)"
                bpm_str = String(bpm.split(separator: " ")[0])
                timestamp = "   "+"\(hkqs.startDate)"
                
                let newData = HeartData(bpm: bpm_str, timestamp: timestamp)
                data += [newData]
            }
        }
        HTTPManager.sendHeartData(data: queryReturned)
        if alsoFetch {
            DispatchQueue.main.asyncAfter(deadline: .now() + 2, execute: {
                self.fetchData()
            })
        }
    }
    
   
    
    //////////////////////////////////////////////////// REFRESHER
    
    lazy var refresher: UIRefreshControl =  {
        let refreshControl = UIRefreshControl()
        refreshControl.tintColor = .black
        refreshControl.addTarget(self, action: #selector(updateData), for: .valueChanged)
        return refreshControl
    }()
    
    @objc
    func updateData(){
        //self.fetchData()
        loadAndSendData(alsoFetch: true)
        tableView.reloadData()
        refresher.endRefreshing()
        
        let deadline = DispatchTime.now() + .milliseconds(500)
        DispatchQueue.main.asyncAfter(deadline: deadline){
            self.refresher.endRefreshing()
        }
        
    }
    
    ////////////////////////////////////////////////////
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.tableView.rowHeight = 50.0
        self.loadAndSendData(alsoFetch: true)
        
        tableView.refreshControl = refresher
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        // #warning Incomplete implementation, return the number of sections
        return 1
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return data.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cellIdentifier = "DataTableViewCell"
        guard let cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier, for: indexPath) as? DataTableViewCell else {
            fatalError("The dequeued cell is not an instance of DataTableViewCell")
        }
        let selectedData = data[indexPath.row]
        
        cell.bpmLabel.text = selectedData.bpm
        cell.timestampLabel.text = selectedData.timestamp
        return cell
    }
    
}
