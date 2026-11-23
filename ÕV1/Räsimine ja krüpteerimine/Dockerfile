FROM python:3.12-slim
RUN pip install --no-cache-dir 'cryptography>=44,<49' 'PyMySQL>=1.1,<2' 'pymongo>=4.8,<5' 'neo4j>=5.26,<6'
COPY lab.py /lab.py
ENTRYPOINT ["python", "/lab.py"]
