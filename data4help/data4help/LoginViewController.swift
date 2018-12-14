import Alamofire
import UIKit

func resetDefaults() {
    let defaults = UserDefaults.standard
    let dictionary = defaults.dictionaryRepresentation()
    dictionary.keys.forEach { key in
        defaults.removeObject(forKey: key)
    }
}


class LoginViewController: UIViewController, UITextFieldDelegate {
    
    var username = ""
    var password = ""
    
    @IBOutlet weak var usernameTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!
    @IBOutlet weak var serverLabel: UILabel!
    
    @IBAction func loginButton(_ sender: UIButton?) {
        username = usernameTextField.text!
        password = passwordTextField.text!
        let credential = URLCredential(user: username, password: password, persistence: .forSession)
        let LOGIN_COMPLETE_URL = Global.getUserURL() + Global.LOGIN_METHOD
        
        Alamofire.request(LOGIN_COMPLETE_URL, method: .post, encoding: JSONEncoding.default)
            .authenticate(usingCredential: credential)
            .responseJSON {
                response in
                
                switch response.result {
                
                // case Alamofire.request fails
                case .failure:
                    let alert = UIAlertController(title: "Attention", message: Messages.LOGIN_ERROR, preferredStyle: .alert)
                    alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
                    self.present(alert, animated: true)
                
                //case Alamogire.request success
                case .success:
                    UserDefaults.standard.set(self.username, forKey: "username")
                    UserDefaults.standard.set(self.password, forKey: "password")
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
                            else { self.performSegue(withIdentifier: "loginToDashboard", sender: nil) }
                        }
                    }
                }
        }
    }
    
    @IBAction func registerButton(_ sender: UIButton) {
        performSegue(withIdentifier: "loginToRegistration", sender: self)
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()  //if desired
        self.loginButton(nil)
        return true
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.passwordTextField.delegate = self //to bind return action on keyboard
        self.hideKeyboardWhenTappedAround() //function to bind the tap out action to the keyboard dismiss action
        resetDefaults() //function do reset user default DEBUGGING PORPOUSE
        Global.getUserURL() {
            () in self.serverLabel.text = Global.getUserURL()
        }
    }
    
}
