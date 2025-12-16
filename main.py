class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
        self.borrowed_by = None  # 记录当前借阅者
    
    def __str__(self):
        status = "可借" if self.is_available else f"已借出给 {self.borrowed_by}"
        return f"《{self.title}》- {self.author} (ISBN: {self.isbn}) - {status}"
    
    def get_info(self):
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'available': self.is_available,
            'borrowed_by': self.borrowed_by
        }


class User:
    def __init__(self, name, card_number):
        self.name = name
        self.card_number = card_number
        self.borrowed_books = []  # 当前借阅的书籍列表
    
    def __str__(self):
        return f"{self.name} (借书卡号: {self.card_number})"
    
    def get_info(self):
        return {
            'name': self.name,
            'card_number': self.card_number,
            'borrowed_count': len(self.borrowed_books),
            'borrowed_books': [book.title for book in self.borrowed_books]
        }


class Library:
    def __init__(self):
        self.books = {}  # ISBN -> Book对象
        self.users = {}  # 卡号 -> User对象
    
    def add_book(self, title, author, isbn):
        """添加书籍到图书馆"""
        if isbn in self.books:
            print(f"错误：ISBN {isbn} 的书籍已存在！")
            return False
        
        book = Book(title, author, isbn)
        self.books[isbn] = book
        print(f"成功添加书籍：《{title}》")
        return True
    
    def register_user(self, name, card_number):
        """注册新用户"""
        if card_number in self.users:
            print(f"错误：借书卡号 {card_number} 已被使用！")
            return False
        
        user = User(name, card_number)
        self.users[card_number] = user
        print(f"成功注册用户：{name}")
        return True
    
    def borrow_book(self, isbn, card_number):
        """借书功能"""
        # 检查书籍是否存在
        if isbn not in self.books:
            print(f"错误：ISBN {isbn} 的书籍不存在！")
            return False
        
        # 检查用户是否存在
        if card_number not in self.users:
            print(f"错误：借书卡号 {card_number} 不存在！")
            return False
        
        book = self.books[isbn]
        user = self.users[card_number]
        
        # 检查书籍是否可借
        if not book.is_available:
            print(f"错误：《{book.title}》已被借出！")
            return False
        
        # 执行借书操作
        book.is_available = False
        book.borrowed_by = user.name
        user.borrowed_books.append(book)
        
        print(f"成功借出：《{book.title}》 -> {user.name}")
        return True
    
    def return_book(self, isbn, card_number):
        """还书功能"""
        # 检查书籍是否存在
        if isbn not in self.books:
            print(f"错误：ISBN {isbn} 的书籍不存在！")
            return False
        
        # 检查用户是否存在
        if card_number not in self.users:
            print(f"错误：借书卡号 {card_number} 不存在！")
            return False
        
        book = self.books[isbn]
        user = self.users[card_number]
        
        # 检查该用户是否借了这本书
        if book not in user.borrowed_books:
            print(f"错误：{user.name} 没有借阅《{book.title}》！")
            return False
        
        # 执行还书操作
        book.is_available = True
        book.borrowed_by = None
        user.borrowed_books.remove(book)
        
        print(f"成功归还：《{book.title}》 <- {user.name}")
        return True
    
    def check_availability(self, isbn):
        """检查某本书是否可借"""
        if isbn not in self.books:
            print(f"错误：ISBN {isbn} 的书籍不存在！")
            return None
        
        book = self.books[isbn]
        if book.is_available:
            print(f"《{book.title}》可借")
            return True
        else:
            print(f"《{book.title}》已借出给 {book.borrowed_by}")
            return False
    
    def display_all_books(self):
        """显示所有书籍"""
        print("\n=== 图书馆藏书列表 ===")
        if not self.books:
            print("图书馆暂无藏书")
            return
        
        for book in self.books.values():
            print(book)
        print()
    
    def display_all_users(self):
        """显示所有用户信息"""
        print("\n=== 注册用户列表 ===")
        if not self.users:
            print("暂无注册用户")
            return
        
        for user in self.users.values():
            info = user.get_info()
            print(f"{user}")
            print(f"  已借书籍数量: {info['borrowed_count']}")
            if info['borrowed_books']:
                print(f"  借阅书籍: {', '.join(info['borrowed_books'])}")
        print()
    
    def find_book_by_title(self, title):
        """根据书名查找书籍"""
        found_books = []
        for book in self.books.values():
            if title.lower() in book.title.lower():
                found_books.append(book)
        
        if found_books:
            print(f"\n找到 {len(found_books)} 本相关书籍:")
            for book in found_books:
                print(f"  {book}")
        else:
            print(f"未找到包含 '{title}' 的书籍")
        
        return found_books


# 演示使用示例
def main():
    # 创建图书馆实例
    library = Library()
    
    # 添加一些书籍
    library.add_book("Python编程从入门到实践", "Eric Matthes", "9787115428028")
    library.add_book("算法导论", "Thomas H. Cormen", "9787111407010")
    library.add_book("设计模式", "Erich Gamma", "9787111075776")
    library.add_book("深入理解计算机系统", "Randal E. Bryant", "9787111321330")
    
    # 注册一些用户
    library.register_user("张三", "CARD001")
    library.register_user("李四", "CARD002")
    library.register_user("王五", "CARD003")
    
    print("\n" + "="*50)
    print("图书馆系统演示")
    print("="*50)
    
    # 显示所有书籍和用户
    library.display_all_books()
    library.display_all_users()
    
    # 检查书籍可用性
    print("检查书籍可用性:")
    library.check_availability("9787115428028")  # Python编程
    library.check_availability("9787111407010")  # 算法导论
    
    # 借书操作
    print("\n借书操作:")
    library.borrow_book("9787115428028", "CARD001")  # 张三借Python书
    library.borrow_book("9787111407010", "CARD002")  # 李四借算法导论
    
    # 再次检查可用性
    print("\n再次检查书籍可用性:")
    library.check_availability("9787115428028")  # Python编程
    
    # 尝试重复借书（应该失败）
    print("\n尝试重复借书:")
    library.borrow_book("9787115428028", "CARD003")  # 王五尝试借已被借出的书
    
    # 还书操作
    print("\n还书操作:")
    library.return_book("9787115428028", "CARD001")  # 张三还书
    
    # 再次检查可用性
    print("\n还书后检查可用性:")
    library.check_availability("9787115428028")  # Python编程
    
    # 按书名搜索
    print("\n按书名搜索:")
    library.find_book_by_title("Python")
    
    # 显示最终状态
    library.display_all_books()
    library.display_all_users()


if __name__ == "__main__":
    main()# 在这里编写代码
