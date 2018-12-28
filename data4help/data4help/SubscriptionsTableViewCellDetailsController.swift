//
//  SubscriptionsTableViewCellDetailsController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 28/12/2018.
//  Copyright © 2018 Francesco Peressini. All rights reserved.
//

import UIKit

class SubscriptionsTableViewCellDetailsController: UIViewController {

    @IBOutlet weak var requesterValueLabel: UILabel!
    @IBOutlet weak var statusValueLabel: UILabel!
    @IBOutlet weak var descriptionValueLabel: UILabel!
    
    var requesterValue : String = ""
    var statusValue : String = ""
    var descriptionValue : String = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()
        requesterValueLabel.text = requesterValue
        statusValueLabel.text = statusValue
        descriptionValueLabel.text = descriptionValue
    }
    
}
