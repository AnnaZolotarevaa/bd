# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from sqlalchemy import exc
# from models import SessionLocal, Book
# from schemas import BookCreate, Book as BookSchema

# app = FastAPI()

# # Функция для получения сессии базы данных
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Create - создание новой книги
# @app.post("/books/", response_model=BookSchema)
# def create_book(book: BookCreate, db: Session = Depends(get_db)):
#     db_book = Book(title=book.title, author=book.author, description=book.description)
#     db.add(db_book)
#     db.commit()
#     db.refresh(db_book)
#     return db_book

# # Read - получение списка всех книг
# @app.get("/books/", response_model=list[BookSchema])
# def get_books(db: Session = Depends(get_db)):
#     books = db.query(Book).all()
#     return books

# # Read - получение книги по ID
# @app.get("/books/{book_id}", response_model=BookSchema)
# def get_book(book_id: int, db: Session = Depends(get_db)):
#     db_book = db.query(Book).filter(Book.id == book_id).first()
#     if db_book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return db_book

# # Update - обновление данных книги
# @app.put("/books/{book_id}", response_model=BookSchema)
# def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
#     db_book = db.query(Book).filter(Book.id == book_id).first()
#     if db_book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
    
#     db_book.title = book.title
#     db_book.author = book.author
#     db_book.description = book.description
    
#     db.commit()
#     db.refresh(db_book)
#     return db_book

# # Delete - удаление книги
# @app.delete("/books/{book_id}")
# def delete_book(book_id: int, db: Session = Depends(get_db)):
#     db_book = db.query(Book).filter(Book.id == book_id).first()
#     if db_book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
    
#     db.delete(db_book)
#     db.commit()
#     return {"message": "Book deleted successfully"}



from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, TransportType, Route, Path

# DATABASE_URL = "sqlite:///./test.db"  # Замените на вашу строку подключения
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/transport"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create - создание нового вида транспорта
@app.post("/transport-types/")
def create_transport_type(name: str, average_speed: float, fuel_consumption: float, vehicle_count: int, db: Session = Depends(get_db)):
    transport_type = TransportType(
        name=name,
        average_speed=average_speed,
        fuel_consumption=fuel_consumption,
        vehicle_count=vehicle_count
    )
    db.add(transport_type)
    db.commit()
    db.refresh(transport_type)
    return transport_type

# Read - получение всех видов транспорта
@app.get("/transport-types/")
def get_transport_types(db: Session = Depends(get_db)):
    return db.query(TransportType).all()

# Create - создание маршрута
@app.post("/routes/")
def create_route(route_number: str, daily_passenger_count: int, fare: float, vehicles_on_route: int, transport_type_id: int, db: Session = Depends(get_db)):
    route = Route(
        route_number=route_number,
        daily_passenger_count=daily_passenger_count,
        fare=fare,
        vehicles_on_route=vehicles_on_route,
        transport_type_id=transport_type_id
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

# Read - получение маршрутов
@app.get("/routes/")
def get_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()

# Create - создание пути
@app.post("/paths/")
def create_path(start_point: str, end_point: str, stops_count: int, distance: float, route_id: int, db: Session = Depends(get_db)):
    path = Path(
        start_point=start_point,
        end_point=end_point,
        stops_count=stops_count,
        distance=distance,
        route_id=route_id
    )
    db.add(path)
    db.commit()
    db.refresh(path)
    return path

# Read - получение всех путей
@app.get("/paths/")
def get_paths(db: Session = Depends(get_db)):
    return db.query(Path).all()

# Read - получение маршрута с деталями пути
@app.get("/routes/{route_id}")
def get_route_with_path(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return {
        "route": route,
        "path": route.path
    }

# Delete - удаление вида транспорта
@app.delete("/transport-types/{transport_type_id}")
def delete_transport_type(transport_type_id: int, db: Session = Depends(get_db)):
    transport_type = db.query(TransportType).filter(TransportType.id == transport_type_id).first()
    if not transport_type:
        raise HTTPException(status_code=404, detail="Transport type not found")
    db.delete(transport_type)
    db.commit()
    return {"message": "Transport type deleted successfully"}


from sqlalchemy import text

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Попробуем выполнить простой запрос к базе
        result = db.execute(text("SELECT 1")).scalar()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

