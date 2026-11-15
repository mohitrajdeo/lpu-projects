"""
Batch convert all generated .docx reports and manuals to .pdf via Microsoft Word COM automation,
then mirror them into the unified dashboard static directories.
"""

import os
import sys
import shutil
import time
import win32com.client

DOCS_TO_CONVERT = [
    # DL Reports
    (r"c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\final_report\FINAL_PROJECT_REPORT.docx",
     r"c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\final_report\FINAL_PROJECT_REPORT.pdf"),
    (r"c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\final_report\FINAL_PROJECT_REPORT.docx",
     r"c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\final_report\FINAL_PROJECT_REPORT.pdf"),
    (r"c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\final_report\FINAL_PROJECT_REPORT.docx",
     r"c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\final_report\FINAL_PROJECT_REPORT.pdf"),
    (r"c:\MOHIT\dl\HOW_TO_USE_AND_EXECUTION_MANUAL.docx",
     r"c:\MOHIT\dl\HOW_TO_USE_AND_EXECUTION_MANUAL.pdf"),
    
    # DevOps Reports
    (r"c:\MOHIT\devops\1_Mohit_Terraform_Nagios\final_report\FINAL_PROJECT_REPORT.docx",
     r"c:\MOHIT\devops\1_Mohit_Terraform_Nagios\final_report\FINAL_PROJECT_REPORT.pdf"),
    (r"c:\MOHIT\devops\2_Akash_Puppet_Nagios\final_report\FINAL_PROJECT_REPORT.docx",
     r"c:\MOHIT\devops\2_Akash_Puppet_Nagios\final_report\FINAL_PROJECT_REPORT.pdf"),
    (r"c:\MOHIT\devops\3_Saif_Terraform_ALB_Nagios\final_report\FINAL_PROJECT_REPORT.docx",
     r"c:\MOHIT\devops\3_Saif_Terraform_ALB_Nagios\final_report\FINAL_PROJECT_REPORT.pdf"),
    (r"c:\MOHIT\devops\HOW_TO_USE_AND_EXECUTION_MANUAL.docx",
     r"c:\MOHIT\devops\HOW_TO_USE_AND_EXECUTION_MANUAL.pdf"),
]

def convert_all():
    print("[*] Starting Word COM automation for PDF conversion...")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False

    try:
        for docx_path, pdf_path in DOCS_TO_CONVERT:
            if not os.path.exists(docx_path):
                print(f"[!] Warning: File not found: {docx_path}")
                continue
            
            abs_docx = os.path.abspath(docx_path)
            abs_pdf = os.path.abspath(pdf_path)
            print(f"[*] Converting: {os.path.basename(abs_docx)} -> {os.path.basename(abs_pdf)}")

            doc = word.Documents.Open(abs_docx, ReadOnly=True)
            # wdFormatPDF = 17
            doc.SaveAs(abs_pdf, FileFormat=17)
            doc.Close(SaveChanges=False)
            print(f"    [OK] PDF Created ({os.path.getsize(abs_pdf)} bytes)")

    finally:
        word.Quit()
        print("[*] Word COM instance closed.")

def mirror_to_dashboard():
    print("[*] Mirroring updated reports to Unified Dashboard static directory...")
    # DL Reports
    dl_map = {
        r"c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\final_report\FINAL_PROJECT_REPORT.docx": r"c:\MOHIT\dl\dashboard\static\reports\mohit.docx",
        r"c:\MOHIT\dl\1_Mohit_AIOps_Cloud_Intelligence\final_report\FINAL_PROJECT_REPORT.pdf": r"c:\MOHIT\dl\dashboard\static\reports\mohit.pdf",
        r"c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\final_report\FINAL_PROJECT_REPORT.docx": r"c:\MOHIT\dl\dashboard\static\reports\akash.docx",
        r"c:\MOHIT\dl\2_Akash_Autonomous_SWE_System\final_report\FINAL_PROJECT_REPORT.pdf": r"c:\MOHIT\dl\dashboard\static\reports\akash.pdf",
        r"c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\final_report\FINAL_PROJECT_REPORT.docx": r"c:\MOHIT\dl\dashboard\static\reports\saif.docx",
        r"c:\MOHIT\dl\3_Saif_Cyber_Threat_Intelligence\final_report\FINAL_PROJECT_REPORT.pdf": r"c:\MOHIT\dl\dashboard\static\reports\saif.pdf",
        r"c:\MOHIT\dl\HOW_TO_USE_AND_EXECUTION_MANUAL.docx": r"c:\MOHIT\dl\dashboard\static\reports\HOW_TO_USE_AND_EXECUTION_MANUAL.docx",
        r"c:\MOHIT\dl\HOW_TO_USE_AND_EXECUTION_MANUAL.pdf": r"c:\MOHIT\dl\dashboard\static\reports\HOW_TO_USE_AND_EXECUTION_MANUAL.pdf",
    }

    # DevOps Reports
    devops_map = {
        r"c:\MOHIT\devops\1_Mohit_Terraform_Nagios\final_report\FINAL_PROJECT_REPORT.docx": r"c:\MOHIT\dl\dashboard\static\devops\mohit_devops.docx",
        r"c:\MOHIT\devops\1_Mohit_Terraform_Nagios\final_report\FINAL_PROJECT_REPORT.pdf": r"c:\MOHIT\dl\dashboard\static\devops\mohit_devops.pdf",
        r"c:\MOHIT\devops\2_Akash_Puppet_Nagios\final_report\FINAL_PROJECT_REPORT.docx": r"c:\MOHIT\dl\dashboard\static\devops\akash_devops.docx",
        r"c:\MOHIT\devops\2_Akash_Puppet_Nagios\final_report\FINAL_PROJECT_REPORT.pdf": r"c:\MOHIT\dl\dashboard\static\devops\akash_devops.pdf",
        r"c:\MOHIT\devops\3_Saif_Terraform_ALB_Nagios\final_report\FINAL_PROJECT_REPORT.docx": r"c:\MOHIT\dl\dashboard\static\devops\saif_devops.docx",
        r"c:\MOHIT\devops\3_Saif_Terraform_ALB_Nagios\final_report\FINAL_PROJECT_REPORT.pdf": r"c:\MOHIT\dl\dashboard\static\devops\saif_devops.pdf",
        r"c:\MOHIT\devops\HOW_TO_USE_AND_EXECUTION_MANUAL.docx": r"c:\MOHIT\dl\dashboard\static\devops\HOW_TO_USE_AND_EXECUTION_MANUAL.docx",
        r"c:\MOHIT\devops\HOW_TO_USE_AND_EXECUTION_MANUAL.pdf": r"c:\MOHIT\dl\dashboard\static\devops\HOW_TO_USE_AND_EXECUTION_MANUAL.pdf",
    }

    os.makedirs(r"c:\MOHIT\dl\dashboard\static\reports", exist_ok=True)
    os.makedirs(r"c:\MOHIT\dl\dashboard\static\devops", exist_ok=True)

    for src, dst in dl_map.items():
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"    [Copied DL Report] -> {os.path.basename(dst)}")

    for src, dst in devops_map.items():
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"    [Copied DevOps Report] -> {os.path.basename(dst)}")

if __name__ == "__main__":
    convert_all()
    mirror_to_dashboard()
    print("[SUCCESS] All PDF conversions and mirrors completed!")

