//
//  SOSViewController.swift
//  data4help
//
//  Created by Alessandro Nichelini on 08/01/2019.
//  Copyright © 2019 Francesco Peressini. All rights reserved.
//

import UIKit

class SOSViewController: UIViewController {

    @IBOutlet weak var label: UILabel!
    @IBOutlet weak var okButton: UIButton!
    
    @IBAction func buttonPressedAction(_ sender: Any) {
        self.dismiss(animated: true, completion: nil)
    }
    
    @objc func timerDoneAction(){
        let alert = UIAlertController(title: "Attention", message: Messages.FIRST_AIDS_CALLED, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: {(action:UIAlertAction) in self.dismiss(animated: true, completion: nil)}))
        self.present(alert, animated: true)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.backgroundColor = .yellow
        if sosTimer != nil {sosTimer.invalidate()}
        sosTimer = Timer.scheduledTimer(timeInterval: 5, target: self, selector: #selector(timerDoneAction), userInfo: nil, repeats: false)
    }
}
