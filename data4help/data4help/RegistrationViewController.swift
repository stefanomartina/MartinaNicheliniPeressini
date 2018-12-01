import Alamofire
import UIKit

class RegistrationViewController: UIViewController {
    
    let URL_USER_REGISTER = "http://localhost:5000/api/users/register"
    
    @IBOutlet weak var textFieldFirstName: UITextField!
    @IBOutlet weak var textFieldLastName: UITextField!
    @IBOutlet weak var textFieldUsername: UITextField!
    @IBOutlet weak var textFieldPassword: UITextField!
    @IBOutlet weak var labelMessage: UILabel!
    
    @IBAction func buttonRegister(_ sender: UIButton) {
        let parameters : Parameters=[
            "firstname":textFieldFirstName.text!,
            "lastname":textFieldLastName.text!,
            "username":textFieldUsername.text!,
            "password":textFieldPassword.text!
        ]
        Alamofire.request(URL_USER_REGISTER, method: .post, parameters: parameters, encoding: JSONEncoding.default)
            .responseJSON {
                response in
                if let status = response.result.value {
                    let JSON = status as! NSDictionary;
                    let appo = JSON["Response"]!;
                    print(appo)
                }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib .
    }
    
}
