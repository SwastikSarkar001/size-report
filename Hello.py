from sizereport import SizeReport
import time

# path = input("Enter the path of the folder to analyse its contents: ")

tstart = time.perf_counter()
a = SizeReport(path=r"C:")
tend = time.perf_counter()
tdiff = round(tend - tstart - 3)
print(f"Process duration: {str(int(tdiff//3600)) + " hrs " if tdiff//3600 != 0 else ""}{str(int(tdiff//60%60)) + " mins " if tdiff//60%60 != 0 else ""}{int(tdiff%60)} secs")
a.write_csv()