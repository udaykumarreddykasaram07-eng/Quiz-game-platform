-- ========================================
-- SAMPLE DATA FOR QUIZ GAME PLATFORM
-- ========================================
-- File: database/sample_data.sql

-- Insert Categories
INSERT INTO categories (category_name, category_description, category_image) VALUES
('General Knowledge', 'Test your general knowledge', 'general.png'),
('Science', 'Physics, Chemistry, Biology questions', 'science.png'),
('History', 'World history and events', 'history.png'),
('Geography', 'Countries, capitals, and landmarks', 'geography.png'),
('Sports', 'Sports trivia and facts', 'sports.png'),
('Entertainment', 'Movies, music, and celebrities', 'entertainment.png'),
('Technology', 'Computers, gadgets, and tech', 'technology.png'),
('Mathematics', 'Math problems and puzzles', 'math.png');

-- Insert Sample Questions - General Knowledge (10 questions)
INSERT INTO questions (category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, points) VALUES
(1, 'What is the capital of France?', 'London', 'Berlin', 'Paris', 'Madrid', 'C', 'easy', 10),
(1, 'Which planet is known as the Red Planet?', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'B', 'easy', 10),
(1, 'Who painted the Mona Lisa?', 'Vincent van Gogh', 'Pablo Picasso', 'Leonardo da Vinci', 'Michelangelo', 'C', 'medium', 15),
(1, 'What is the largest ocean on Earth?', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean', 'D', 'easy', 10),
(1, 'Which element has the chemical symbol O?', 'Gold', 'Oxygen', 'Silver', 'Iron', 'B', 'easy', 10),
(1, 'What is the smallest prime number?', '0', '1', '2', '3', 'C', 'medium', 15),
(1, 'Who wrote Romeo and Juliet?', 'Charles Dickens', 'Mark Twain', 'William Shakespeare', 'Jane Austen', 'C', 'medium', 15),
(1, 'What is the currency of Japan?', 'Yuan', 'Won', 'Yen', 'Ringgit', 'C', 'medium', 15),
(1, 'Which country is known as the Land of the Rising Sun?', 'China', 'South Korea', 'Thailand', 'Japan', 'D', 'easy', 10),
(1, 'What is the largest mammal in the world?', 'Elephant', 'Blue Whale', 'Giraffe', 'Polar Bear', 'B', 'easy', 10);

-- Insert Sample Questions - Science (10 questions)
INSERT INTO questions (category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, points) VALUES
(2, 'What is the chemical symbol for water?', 'H2O', 'CO2', 'O2', 'NaCl', 'A', 'easy', 10),
(2, 'Which gas do plants absorb from the atmosphere?', 'Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Hydrogen', 'C', 'easy', 10),
(2, 'What is the hardest natural substance on Earth?', 'Gold', 'Iron', 'Diamond', 'Quartz', 'C', 'medium', 15),
(2, 'Which planet is closest to the Sun?', 'Venus', 'Earth', 'Mercury', 'Mars', 'C', 'easy', 10),
(2, 'What is the pH value of pure water?', '5', '7', '9', '14', 'B', 'medium', 15),
(2, 'Which organ pumps blood throughout the body?', 'Liver', 'Brain', 'Heart', 'Lungs', 'C', 'easy', 10),
(2, 'What is the speed of light?', '300,000 km/s', '150,000 km/s', '450,000 km/s', '600,000 km/s', 'A', 'hard', 20),
(2, 'Which metal is liquid at room temperature?', 'Iron', 'Mercury', 'Gold', 'Copper', 'B', 'medium', 15),
(2, 'What is the main component of natural gas?', 'Methane', 'Ethane', 'Propane', 'Butane', 'A', 'medium', 15),
(2, 'Which scientist developed the theory of relativity?', 'Isaac Newton', 'Albert Einstein', 'Galileo Galilei', 'Stephen Hawking', 'B', 'medium', 15);

-- Insert Sample Questions - History (10 questions)
INSERT INTO questions (category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, points) VALUES
(3, 'Who was the first President of the United States?', 'Thomas Jefferson', 'John Adams', 'George Washington', 'Abraham Lincoln', 'C', 'easy', 10),
(3, 'In which year did World War II end?', '1943', '1944', '1945', '1946', 'C', 'medium', 15),
(3, 'Which ancient civilization built the pyramids?', 'Romans', 'Greeks', 'Egyptians', 'Mayans', 'C', 'easy', 10),
(3, 'Who discovered America in 1492?', 'Vasco da Gama', 'Christopher Columbus', 'Marco Polo', 'Ferdinand Magellan', 'B', 'easy', 10),
(3, 'Which empire was ruled by Genghis Khan?', 'Roman Empire', 'Ottoman Empire', 'Mongol Empire', 'British Empire', 'C', 'medium', 15),
(3, 'The Industrial Revolution began in which country?', 'France', 'Germany', 'United States', 'Great Britain', 'D', 'medium', 15),
(3, 'Who was the last Tsar of Russia?', 'Peter the Great', 'Nicholas II', 'Ivan the Terrible', 'Catherine the Great', 'B', 'hard', 20),
(3, 'The Berlin Wall fell in which year?', '1987', '1988', '1989', '1990', 'C', 'medium', 15),
(3, 'Which war was fought between North and South Korea?', 'Vietnam War', 'Cold War', 'Korean War', 'Gulf War', 'C', 'easy', 10),
(3, 'Who was known as the "Iron Lady"?', 'Angela Merkel', 'Indira Gandhi', 'Margaret Thatcher', 'Golda Meir', 'C', 'medium', 15);

-- Insert Sample Questions - Geography (10 questions)
INSERT INTO questions (category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, points) VALUES
(4, 'What is the capital of Australia?', 'Sydney', 'Melbourne', 'Canberra', 'Perth', 'C', 'medium', 15),
(4, 'Which is the longest river in the world?', 'Amazon River', 'Nile River', 'Yangtze River', 'Mississippi River', 'B', 'easy', 10),
(4, 'Mount Everest is located in which mountain range?', 'Andes', 'Alps', 'Himalayas', 'Rockies', 'C', 'easy', 10),
(4, 'Which country has the largest population?', 'India', 'United States', 'China', 'Russia', 'C', 'easy', 10),
(4, 'What is the smallest country in the world?', 'Monaco', 'Malta', 'Vatican City', 'San Marino', 'C', 'medium', 15),
(4, 'Which desert is the largest in the world?', 'Gobi Desert', 'Sahara Desert', 'Arabian Desert', 'Kalahari Desert', 'B', 'easy', 10),
(4, 'The Great Barrier Reef is located off the coast of which country?', 'Brazil', 'Australia', 'Mexico', 'Indonesia', 'B', 'easy', 10),
(4, 'Which continent is also a country?', 'Africa', 'Europe', 'Australia', 'Antarctica', 'C', 'easy', 10),
(4, 'What is the capital of Canada?', 'Toronto', 'Vancouver', 'Ottawa', 'Montreal', 'C', 'medium', 15),
(4, 'Which ocean is the smallest?', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Southern Ocean', 'C', 'medium', 15);

-- Insert Sample Questions - Sports (10 questions)
INSERT INTO questions (category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, points) VALUES
(5, 'Which country won the FIFA World Cup in 2022?', 'Brazil', 'France', 'Argentina', 'Germany', 'C', 'medium', 15),
(5, 'Who holds the record for most Olympic gold medals?', 'Michael Phelps', 'Usain Bolt', 'Simone Biles', 'Carl Lewis', 'A', 'easy', 10),
(5, 'Which tennis player has won the most Grand Slam singles titles?', 'Roger Federer', 'Rafael Nadal', 'Novak Djokovic', 'Serena Williams', 'C', 'medium', 15),
(5, 'In which sport would you perform a "slam dunk"?', 'Soccer', 'Tennis', 'Basketball', 'Golf', 'C', 'easy', 10),
(5, 'Which NBA team has won the most championships?', 'Los Angeles Lakers', 'Boston Celtics', 'Chicago Bulls', 'Golden State Warriors', 'B', 'medium', 15),
(5, 'What is the diameter of a basketball hoop in inches?', '16 inches', '18 inches', '20 inches', '24 inches', 'B', 'hard', 20),
(5, 'Which country invented volleyball?', 'United States', 'Brazil', 'Japan', 'Australia', 'A', 'medium', 15),
(5, 'How many players are on the field for one team in a soccer match?', '9', '10', '11', '12', 'C', 'easy', 10),
(5, 'Which golfer has won the most major championships?', 'Jack Nicklaus', 'Tiger Woods', 'Arnold Palmer', 'Ben Hogan', 'A', 'hard', 20),
(5, 'In cricket, how many balls are in an over?', '4', '5', '6', '8', 'C', 'easy', 10);

-- Insert Sample Questions - Entertainment (10 questions)
INSERT INTO questions (category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, points) VALUES
(6, 'Which actor played Iron Man in the Marvel Cinematic Universe?', 'Chris Evans', 'Chris Hemsworth', 'Robert Downey Jr.', 'Mark Ruffalo', 'C', 'easy', 10),
(6, 'What is the highest-grossing film of all time (not adjusted for inflation)?', 'Avatar', 'Avengers: Endgame', 'Titanic', 'Star Wars: The Force Awakens', 'A', 'medium', 15),
(6, 'Who directed the movie "Inception"?', 'Steven Spielberg', 'James Cameron', 'Christopher Nolan', 'Quentin Tarantino', 'C', 'easy', 10),
(6, 'Which band performed the song "Bohemian Rhapsody"?', 'The Beatles', 'Led Zeppelin', 'Queen', 'Pink Floyd', 'C', 'easy', 10),
(6, 'What year was the first Harry Potter film released?', '1997', '2001', '2003', '2005', 'B', 'medium', 15),
(6, 'Which actress won an Oscar for her role in "La La Land"?', 'Emma Stone', 'Emma Watson', 'Jennifer Lawrence', 'Meryl Streep', 'A', 'medium', 15),
(6, 'What is the name of the fictional African country in "Black Panther"?', 'Wakanda', 'Zamunda', 'Genovia', 'Elbonia', 'A', 'easy', 10),
(6, 'Which TV show features the characters Sheldon Cooper and Leonard Hofstadter?', 'The Big Bang Theory', 'Friends', 'How I Met Your Mother', 'The Office', 'A', 'easy', 10),
(6, 'Who composed the soundtrack for "The Lord of the Rings" trilogy?', 'John Williams', 'Hans Zimmer', 'Howard Shore', 'Ennio Morricone', 'C', 'hard', 20),
(6, 'Which streaming service produced "Stranger Things"?', 'Hulu', 'Amazon Prime', 'Disney+', 'Netflix', 'D', 'easy', 10);

-- Insert Sample Questions - Technology (10 questions)
INSERT INTO questions (category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, points) VALUES
(7, 'What does "HTTP" stand for?', 'Hyper Text Transfer Protocol', 'High Tech Transfer Protocol', 'Hyperlink Text Transmission Protocol', 'Home Tool Transfer Protocol', 'A', 'easy', 10),
(7, 'Who is the co-founder of Apple Inc.?', 'Bill Gates', 'Steve Jobs', 'Mark Zuckerberg', 'Elon Musk', 'B', 'easy', 10),
(7, 'What year was the first iPhone released?', '2005', '2007', '2009', '2010', 'B', 'medium', 15),
(7, 'Which programming language was created by Guido van Rossum?', 'Java', 'Python', 'Ruby', 'JavaScript', 'B', 'medium', 15),
(7, 'What does "AI" stand for?', 'Automated Intelligence', 'Artificial Intelligence', 'Advanced Interface', 'Algorithmic Integration', 'B', 'easy', 10),
(7, 'Which company developed the Android operating system?', 'Apple', 'Microsoft', 'Google', 'Samsung', 'C', 'easy', 10),
(7, 'What is the name of the first web browser?', 'Internet Explorer', 'Netscape Navigator', 'Mosaic', 'WorldWideWeb', 'D', 'hard', 20),
(7, 'How many bits are in one byte?', '4', '8', '16', '32', 'B', 'medium', 15),
(7, 'What does "URL" stand for?', 'Universal Resource Locator', 'Uniform Resource Locator', 'United Resource Link', 'Universal Reference Link', 'B', 'medium', 15),
(7, 'Which technology company was founded by Larry Page and Sergey Brin?', 'Facebook', 'Amazon', 'Microsoft', 'Google', 'D', 'easy', 10);

-- Insert Sample Questions - Mathematics (10 questions)
INSERT INTO questions (category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty_level, points) VALUES
(8, 'What is the value of π (pi) rounded to two decimal places?', '3.14', '3.16', '3.18', '3.20', 'A', 'easy', 10),
(8, 'What is the square root of 144?', '10', '11', '12', '13', 'C', 'easy', 10),
(8, 'What is the sum of angles in a triangle?', '90 degrees', '180 degrees', '270 degrees', '360 degrees', 'B', 'easy', 10),
(8, 'What is 15% of 200?', '15', '20', '25', '30', 'D', 'medium', 15),
(8, 'What is the next number in the sequence: 2, 4, 8, 16, ___?', '24', '30', '32', '64', 'C', 'medium', 15),
(8, 'What is the area of a circle with radius 5? (Use π=3.14)', '31.4', '62.8', '78.5', '157', 'C', 'hard', 20),
(8, 'Solve for x: 2x + 5 = 15', 'x = 5', 'x = 7', 'x = 10', 'x = 12', 'A', 'medium', 15),
(8, 'What is the probability of rolling a 6 on a standard die?', '1/2', '1/4', '1/6', '1/8', 'C', 'medium', 15),
(8, 'What is the value of 5! (5 factorial)?', '20', '60', '100', '120', 'D', 'hard', 20),
(8, 'Which of these numbers is a prime number?', '21', '23', '25', '27', 'B', 'medium', 15);