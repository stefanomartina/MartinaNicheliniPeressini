import Alamofire
import UIKit

class LoginViewController: UIViewController {
    
    var username = ""
    var password = ""
    
    @IBOutlet weak var usernameTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!
    @IBOutlet weak var serverLabel: UILabel!
    
    @IBAction func loginButton(_ sender: UIButton) {
        username = usernameTextField.text!
        password = passwordTextField.text!
        let credential = URLCredential(user: username, password: password, persistence: .forSession)
        let LOGIN_COMPLETE_URL = Global.getUserURL() + Global.LOGIN_METHOD
        
        Alamofire.request(LOGIN_COMPLETE_URL, method: .post, encoding: JSONEncoding.default)
            .authenticate(usingCredential: credential)
            .responseJSON {
                response in
                
                if let status = response.result.value {
                    let JSON = status as! NSDictionary
                    
                    if let result = JSON["Response"] as? String {
                        if(result == "-1") {
                            if let message = JSON["Message"] as? String {
                                let alert = UIAlertController(title: "Attention", message: message, preferredStyle: .alert)
                                alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
                                self.present(alert, animated: true)
                            }
                        }
                        else {
                            self.performSegue(withIdentifier: "loginToDashboard", sender: nil)
                        }
                    }
                }
        }
    }
    
    @IBAction func registerButton(_ sender: UIButton) {
        performSegue(withIdentifier: "loginToRegistration", sender: self)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        Global.getUserURL() {
            () in self.serverLabel.text = Global.getUserURL()
        }
    }
    
}
