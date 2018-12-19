//
//  SubscriptionTableViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 16/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit


class SubscriptionTableViewController: UITableViewController {
    
    var tableViewData = [subscribtionRequest]()
    
    override func viewDidLoad() {
        HTTPManager.getSubscribtion { returned in
            self.tableViewData = returned 
        }
        super.viewDidLoad()
        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
        // self.navigationItem.rightBarButtonItem = self.editButtonItem
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        return tableViewData.count
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // #warning Incomplete implementation, return the number of rows
        return 0
    }


}
