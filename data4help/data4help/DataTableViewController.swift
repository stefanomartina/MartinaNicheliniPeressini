//
//  DataTableViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 22/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit
import HealthKit


class DataTableViewController: UITableViewController{
    
    var data = [Data]()
    
    ////////////////////////////////////////////////////
    private func fetchData(){
        self.data = []
        HTTPManager.getHearthDataFromDB { retrievedData in
            self.data = self.data + retrievedData
            HTTPManager.getLocationDataFromDb{ retrievedData in
                self.data = self.data + retrievedData
                self.data = self.data.sorted(by: {
                    $0.timestamp.compare($1.timestamp) == .orderedDescending
                })
                self.tableView.reloadData()
            }
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
        //loadAndSendData(alsoFetch: true)
        self.fetchData()
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
        self.fetchData()
        self.tableView.reloadData()
        
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
        let heartCellIdentifier = "DataTableViewCell"
        let locationCellIdentifier = "LocationDataTableViewCell"
        
        let selectedData = data[indexPath.row]
        
        if type(of: data[indexPath.row]) == HeartData.self {
            guard let cell = tableView.dequeueReusableCell(withIdentifier: heartCellIdentifier, for: indexPath) as? DataTableViewCell else {fatalError("The dequeued cell is not an instance of DataTableViewCell")}
            
            cell.bpmLabel.text = (selectedData as! HeartData).bpm
            cell.timestampLabel.text = (selectedData as! HeartData).str_timestamp
            if (selectedData as! HeartData).sos {cell.backgroundColor = .yellow}
            return cell
        }
        else {
            guard let cell = tableView.dequeueReusableCell(withIdentifier: locationCellIdentifier, for: indexPath) as? LocationDataTableViewCell else { fatalError("The dequeued cell is not an instance of LocationDataTableViewCell")}
            cell.timestampLabel.text = (selectedData as! LocationData).str_timestamp
            cell.coordinatesLabel.text = "" + String((selectedData as! LocationData).latitude) + " H, " +
                                                String((selectedData as! LocationData).longitude) + " W"
            return cell
        }
    } // end methods
    
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        
        // Get the index path from the cell that was tapped
        let indexPath = tableView.indexPathForSelectedRow
        // Get the Row of the Index Path and set as index
        let index = indexPath?.row
        // Get in touch with the DetailViewController
        let detailViewController = segue.destination as! LocationDataCellDetailsMapViewController
        // Pass on the data to the Detail ViewController by setting it's indexPathRow value
        detailViewController.latitude = (self.data[index!] as! LocationData).latitude
        detailViewController.longitude = (self.data[index!] as! LocationData).longitude
    }
}
