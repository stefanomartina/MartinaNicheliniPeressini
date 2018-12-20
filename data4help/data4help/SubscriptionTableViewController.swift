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
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.tableView.rowHeight = 80.0
        HTTPManager.getSubscribtion { returned in
            self.subscriptions = returned
            self.tableView.reloadData()
        }
    }
    
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
            let shareMenu = UIAlertController(title: nil, message: "Share using",  preferredStyle: .actionSheet)
            let twitterAction = UIAlertAction(title: "Twitter", style: UIAlertAction.Style.default, handler: nil)
            let cancelAction = UIAlertAction(title: "Cancel", style: UIAlertAction.Style.cancel, handler: nil)
            
            shareMenu.addAction(twitterAction)
            shareMenu.addAction(cancelAction)
            
            self.present(shareMenu, animated: true, completion: nil)
        })
        acceptAction.backgroundColor = .green
        
        // 3
        let denyAction = UITableViewRowAction(style: UITableViewRowAction.Style.default, title: "Deny" , handler: { (action:UITableViewRowAction, indexPath:IndexPath) -> Void in
            // 4
            let rateMenu = UIAlertController(title: nil, message: "Rate this App", preferredStyle: .actionSheet)
            
            let appRateAction = UIAlertAction(title: "Rate", style: UIAlertAction.Style.default, handler: nil)
            let cancelAction = UIAlertAction(title: "Cancel", style: UIAlertAction.Style.cancel, handler: nil)
            
            rateMenu.addAction(appRateAction)
            rateMenu.addAction(cancelAction)
            
            self.present(rateMenu, animated: true, completion: nil)
        })
        
        // 5
        return [acceptAction,denyAction]
    }
    
}
