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
    
    private func completion(_ newStatus: subscriptionStatus, _ indexPath: IndexPath){
        HTTPManager.modifySubscriptionStatus(newStatus: newStatus,
                                             thirdPartyID: self.subscriptions[indexPath.row].requesterName
            , {
                response in
                if response {self.updateAll(indexPath)}
                else {self.generateNetworkError()}
        })
    }
    
    ////////////////////////////////////////////////////
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.tableView.rowHeight = 80.0
        self.fetchData()
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
        
        return cell
    }
    
    override func tableView(_ tableView: UITableView, editActionsForRowAt indexPath: IndexPath) -> [UITableViewRowAction]?
    {
        let acceptAction = UITableViewRowAction(style: UITableViewRowAction.Style.default, title: "Accept", handler: { (action:UITableViewRowAction, indexPath: IndexPath) -> Void in
            self.completion(subscriptionStatus.approved, indexPath)})
        acceptAction.backgroundColor = .green
        
        let denyAction = UITableViewRowAction(style: UITableViewRowAction.Style.default, title: "Deny" , handler: { (action:UITableViewRowAction, indexPath:IndexPath) -> Void in self.completion(subscriptionStatus.rejected, indexPath)})

        return [acceptAction,denyAction]
    }
    
}
