//
//  ViewController.swift
//  Data4Help
//
//  Created by Alessandro Nichelini on 26/11/2018.
//  Copyright © 2018 MartinaNicheliniPeressini. All rights reserved.
//

import Alamofire
import UIKit

class ViewController: UIViewController {
    
    let URL_USER_REGISTER = "http://localhost:5000/api/users/register";
    
    @IBOutlet weak var textFieldFirsName: UITextField!
    @IBOutlet weak var textFieldLastName: UITextField!
    @IBOutlet weak var textFieldUsername: UITextField!
    @IBOutlet weak var textFieldPassword: UITextField!
    //@IBOutlet weak var labelMessage: UILabel!
    
    @IBAction func buttonRegister(_ sender: UIButton) {
     
        //creating parameters for the post request
        let parameters : Parameters=[
            "firstName":textFieldFirsName.text!,
            "lastName":textFieldLastName.text!,
            "username":textFieldUsername.text!,
            "password":textFieldPassword.text!
        ]
        
        //Sending http post request
        Alamofire.request(URL_USER_REGISTER, method: .post, parameters: parameters).responseJSON
            {
                response in
                //printing response
                print(response)
                
                //getting the json value from the server
                if let result = response.result.value {
                    
                    //converting it as NSDictionary
                    let jsonData = result as! NSDictionary
                    
                    //displaying the message in label
                   //c self.labelMessage.text = jsonData.value(forKey: "message") as! String?
                }
        }
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}
