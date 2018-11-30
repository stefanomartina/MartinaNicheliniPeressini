import UIKit
import Alamofire

class LoginViewController: UIViewController {
    
    let URL_USER_LOGIN = "http://localhost:5000/api/users/login"
    var username = ""
    var password = ""
    
    @IBOutlet weak var usernameTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!

    @IBAction func loginButton(_ sender: UIButton){
        username = usernameTextField.text!
        password = passwordTextField.text!
        let credential = URLCredential(user: username, password: password, persistence: .forSession)
        
        Alamofire.request(URL_USER_LOGIN, method: .post, encoding: JSONEncoding.default)
            .authenticate(usingCredential: credential)
            .responseJSON {
                response in
                
                if let status = response.result.value{
                    let JSON = status as! NSDictionary
                    
                    if let result = JSON["Response"] as? String{
                        if(result == "-1"){
                            if let message = JSON["Message"] as? String{
                                let alert = UIAlertController(title: "Attention", message: message, preferredStyle: .alert)
                                alert.addAction(UIAlertAction(title: "OK", style: .cancel, handler: nil))
                                self.present(alert, animated: true)
                            }
                        }else{
                            self.performSegue(withIdentifier: "LoginToDashboard", sender: self)
                        }
                    }else{
                        print("non sono entrato")
                    }
                    
                }
            
        
        }
    }
    
    @IBAction func registerButton(_ sender: UIButton) {
        performSegue(withIdentifier: "loginToRegistration", sender: self)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    
    override func viewDidAppear(_ animated: Bool) {
        
    }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
