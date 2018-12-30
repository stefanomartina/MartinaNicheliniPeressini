//
//  SubscriptionTableViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 16/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit


class SubscriptionTableViewController: UITableViewController {
    
    var subscriptions = [subscribtionRequest]()
    
    ////////////////////////////////////////////////////
    
    private func fetchData() {
        HTTPManager.getSubscribtion { returned in
            self.subscriptions = returned
            self.tableView.reloadData()
        }
    }
    
    private func updateAll(_ indexPath: IndexPath){
        self.fetchData()
        tableView.reloadData()
        tableView.reloadRows(at: [indexPath], with: UITableView.RowAnimation.automatic)
    }
    
    private func generateNetworkError(){
        let alert = UIAlertController(title: "Attention", message: Messages.NETWORK_ERROR, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
        self.present(alert, animated: true)
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
        self.tableView.rowHeight = 80.0
        self.fetchData()
        
        
        tableView.refreshControl = refresher
    }
    
    ////////////////////////////////////////////////////
    
    //The first of these is numberOfSections(In:), which tells the table view how many sections to display.
    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    //The first of these is numberOfSections(In:), which tells the table view how many sections to display.
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return subscriptions.count
    }
    
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cellIdentifier = "SubscriptionTableViewCell"
        guard let cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier, for: indexPath) as? SubscriptionTableViewCell else {
            fatalError("The dequeued cell is not an instance of SubscriptionTableViewCell")
        }
        let subscription = subscriptions[indexPath.row]
        
        cell.requesterNameLabel.text = subscription.requesterName
        cell.actualStatusLabel.text = subscription.status.rawValue
        if subscription.status == subscriptionStatus.approved {cell.actualStatusLabel.textColor = UIColor.green}
        else if subscription.status == subscriptionStatus.rejected {cell.actualStatusLabel.textColor = UIColor.red}
        else {cell.actualStatusLabel.textColor = UIColor.black}
        return cell
    }
    
    override func tableView(_ tableView: UITableView, editActionsForRowAt indexPath: IndexPath) -> [UITableViewRowAction]?
    {
        let acceptAction = UITableViewRowAction(style: UITableViewRowAction.Style.default, title: "Accept", handler: { (action:UITableViewRowAction, indexPath: IndexPath) -> Void in self.subscriptions[indexPath.row].approve(successHandler: {self.updateAll(indexPath)}, errorHandler: {self.generateNetworkError()})})
        acceptAction.backgroundColor = .green
        
        let denyAction = UITableViewRowAction(style: UITableViewRowAction.Style.default, title: "Deny" , handler: { (action:UITableViewRowAction, indexPath:IndexPath) -> Void in self.subscriptions[indexPath.row].deny(successHandler: {self.updateAll(indexPath)}, errorHandler: {self.generateNetworkError()})})
        denyAction.backgroundColor = .red
        
        return [acceptAction,denyAction]
    }
    
    ////////////////////////////////////////////////////
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        
        // Get the index path from the cell that was tapped
        let indexPath = tableView.indexPathForSelectedRow
        // Get the Row of the Index Path and set as index
        let index = indexPath?.row
        // Get in touch with the DetailViewController
        let detailViewController = segue.destination as! SubscriptionsTableViewCellDetailsController
        // Pass on the data to the Detail ViewController by setting it's indexPathRow value
        
        detailViewController.requesterValue = self.subscriptions[index!].requesterName
        detailViewController.statusValue = self.subscriptions[index!].status.rawValue
        detailViewController.descriptionValue = self.subscriptions[index!].description
    }
}
