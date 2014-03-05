// main.cp#include "main.h"#include <errno.h>BEGIN_MESSAGE_MAP( CMFCPromptForVariableDlg, CDialog )ON_NOTIFY_EX(TTN_NEEDTEXT, 0, OnToolTipText)ON_BN_CLICKED(IDD_PROMPT_FOR_VARIABLE_GOBACK, OnGoBackPressed)END_MESSAGE_MAP()CEyeDxBooleanType CMFCPromptForVariableDlg::OnToolTipText(UINT, NMHDR* pNMHDR, LRESULT*){	TOOLTIPTEXT *pTTT = (TOOLTIPTEXT *) pNMHDR;	if (!(pTTT->uFlags & TTF_IDISHWND))	// the ID must be a handle to a window		return FALSE;			UINT uID = pNMHDR->idFrom;	uID = ::GetDlgCtrlID((HWND)uID);			CString strTipText;		// Attempt to load a ToolTip string that corresponds to the control's ID		if(!strTipText.LoadString(uID))		return FALSE;		// Stuff text into the ToolTip, 80 characters maximum		strncpy(pTTT->lpszText, strTipText, 80);	return TRUE;}CMFCPromptForVariableDlg::~CMFCPromptForVariableDlg(){	delete m_SortedVariables;}// ---------------------------------------------------------------------------------//		� SetupDialog// ---------------------------------------------------------------------------------const long kDialogXGap = 13;const long kDialogYGap = 13;const long kDialogMaxCaptionWidth = 220;const long kDialogRequiredCaptionWidth = 100;const long kDialogInputFieldWidth = 200;const long kDialogCaptionHeight = 16;const long kDialogInputFieldHeight = 20;// This routine handles both single and multiple prompts for variables. If m_PromptOrder is set to "kNoPromptOrder",// that means that all variables that should be prompted in the current dialog should be prompted in a single// dialog. Otherwise, just the single variable that is specified by the m_PromptOrder should be requested.CEyeDxBooleanType CMFCPromptForVariableDlg::OnInitDialog(){	CRect rect;		CDialog::OnInitDialog();			EnableToolTips(TRUE);	long theLongestCaptionWidth = 0;	long theLongestInputWidth = 0;	long theRequiredCaptionWidth = 0;			// For each variable that is in this dialog, create a caption and an edit field. We first search for	// all prompted variables, adding them to our local sorted list. 	// Once we have that, we look for the longest prompt string. Based on that, we establish the longest 	// caption field. Once we have the longest caption field, we truncate it to no more than 	// kLongestAllowedCaption. Finally, we start building objects.		// As objects are created, the captions are right-aligned, and positioned kDialogXGap pixels away 	// from the edit field. The edit fields are all created with the same kInputFieldWidth, and each is 	// initialized with the variable's default value.		// Finally, once we have created all of the objects, we position the Cancel and OK buttons, and resize the	// dialog window to the appropriate size.		// Create our own variable list, using the sort by prompt order comparator		m_SortedVariables = new CEyeDxVariableList(CEyeDxVariableList::kSortByPromptOrder);		long numVariables = m_VariableList->GetCount();		for (long varNum = 0; varNum < numVariables; varNum++)	{		CEyeDxVariable *theVariable = m_VariableList->GetVariableByIndex(varNum);				// If this variable is in this dialog, add it to our sorted list				if (theVariable->GetWhenToPrompt() == m_PromptType)		{			// If passed kNoPromptOrder, we add all of the variables for this prompt type and dialog			if (m_PromptOrder == kNoPromptOrder)				m_SortedVariables->AddVariable(theVariable);			// Otherwise, we add it only if it's the one we're looking for			else if (m_PromptOrder == theVariable->GetPromptOrder())				m_SortedVariables->AddVariable(theVariable);					}			}		// Now we save the number of prompts and calculate the longest prompt string			m_NumPrompts = m_SortedVariables->GetCount();		for (long numPrompt = 0; numPrompt < m_NumPrompts; numPrompt++)	{		CEyeDxVariable *theVariable = m_SortedVariables->GetVariableByIndex(numPrompt);		CEyeDxShortStringType *thePromptStr = theVariable->GetPromptString();		long theCaptionWidth = CalcTextWidth(*thePromptStr);				// The item is not a checkbox type, we use the prompt string as the caption. For check boxes, the		// prompt string is the checkbox title, and there is no caption				if ((theCaptionWidth > theLongestCaptionWidth) && (theVariable->GetDataType() != CEyeDxVariable::kCheckBox))		{			// At least one variable will have the required indicator			theRequiredCaptionWidth = kDialogRequiredCaptionWidth;			theLongestCaptionWidth = theCaptionWidth;						// If the widest input area width isn't an edit field width yet (all previous items were checkboxes),			// then bump up the width to the edit field width.						if (theLongestInputWidth < kDialogInputFieldWidth)				theLongestInputWidth = kDialogInputFieldWidth;		}				// For checkbox types, we figure out the larger of the largest checkbox title (prompt) string and the		// edit field width.				if ((theCaptionWidth > theLongestInputWidth) && (theVariable->GetDataType() == CEyeDxVariable::kCheckBox))		{			// At least one checkbox has a string longer than this and longer than the edit field width			// We set the width to the width of the string plus some extra space to account for the checkbox			theLongestInputWidth = theCaptionWidth + kDialogXGap + kDialogXGap + kDialogXGap;			}				if ((theVariable->GetDataType() != CEyeDxVariable::kCheckBox) && (theVariable->GetDataType() != CEyeDxVariable::kMenu))		{			// At least one variable will have the required indicator, so change the size from zero			theRequiredCaptionWidth = kDialogRequiredCaptionWidth;		}	}		// Restrict the caption width to a maximum size after making it a bit larger than the widest string		theLongestCaptionWidth += kDialogXGap;		if (theLongestCaptionWidth > kDialogMaxCaptionWidth)		theLongestCaptionWidth = kDialogMaxCaptionWidth;			if (theLongestInputWidth > kDialogInputFieldWidth)		theLongestInputWidth = kDialogInputFieldWidth;			long yPos = kDialogYGap;	long xCaptionPos = kDialogXGap;	long xInputFieldPos = (kDialogXGap + theLongestCaptionWidth + kDialogXGap);	long xRequiredCaptionPos = (xInputFieldPos + theLongestInputWidth + kDialogXGap);		long theFrameHeight;	long theFrameWidth = (kDialogXGap + theLongestCaptionWidth + 						  kDialogXGap + theLongestInputWidth + 						  kDialogXGap + theRequiredCaptionWidth + 						  kDialogXGap);	// All objects in the window will be numbered starting after the Go Back button ID		short theID = IDD_PROMPT_FOR_VARIABLE_GOBACK + 1;		for (long numPrompt = 0; numPrompt < m_NumPrompts; numPrompt++)	{		CEyeDxVariable *theVariable = m_SortedVariables->GetVariableByIndex(numPrompt);				CEyeDxShortStringType *thePromptStr = theVariable->GetPromptString();		// For check boxes, we use the prompt string as the title of the item, and create 				CEyeDxCaptionType *theCaption = NULL;				if (theVariable->GetDataType() != CEyeDxVariable::kCheckBox)		{			// Calculate the size and position of the caption object						short theTop = (yPos + (kDialogInputFieldHeight - kDialogCaptionHeight) / 2);			CRect rect(xCaptionPos, theTop,  (xCaptionPos + theLongestCaptionWidth), (theTop + kDialogCaptionHeight));				theCaption = new CEyeDxCaptionType();			theCaption->Create(*thePromptStr, WS_CHILD | WS_VISIBLE | SS_LEFT, rect, this, theID++);		}		// Add either a real object or NULL to the list							m_LabelCaptions.Add(theCaption);							// Calculate the size and position of the input field object				CEyeDxShortStringType *theDefaultStr = theVariable->GetDefaultValue();		CEdit *theEditField = NULL;		CButton *theCheckBox = NULL;		CComboBox *theChoiceMenu = NULL;		short saveInputHeight;				switch (theVariable->GetDataType())		{		case CEyeDxVariable::kCheckBox:			short theValue = 0;									if (*theDefaultStr == kCheckBoxOnStr)				theValue = 1;			rect.SetRect(xInputFieldPos, yPos, xInputFieldPos + theLongestInputWidth, yPos + kDialogInputFieldHeight);						// Save the height so we can position the next line correctly						saveInputHeight = kDialogInputFieldHeight;			theCheckBox = new CButton();			theCheckBox->Create(*thePromptStr, WS_CHILD | WS_VISIBLE | BS_AUTOCHECKBOX | WS_TABSTOP, rect, this, theID++);			if (theValue)				theCheckBox->SetCheck(BST_CHECKED);			else				theCheckBox->SetCheck(BST_UNCHECKED);						break;					case CEyeDxVariable::kMenu:						rect.SetRect(xInputFieldPos, yPos, xInputFieldPos + theLongestInputWidth, yPos + (kDialogInputFieldHeight * 5));						// Save the height so we can position the next line correctly - note that the object rectangle has to be			// bigger than the entry box along so that the pop-up menu appears						saveInputHeight = kDialogInputFieldHeight;			theChoiceMenu = new CComboBox();			theChoiceMenu->Create(WS_CHILD | WS_VISIBLE | WS_BORDER | WS_VSCROLL | CBS_DROPDOWNLIST | WS_TABSTOP, rect, this, theID++);																						theChoiceMenu->SetExtendedUI(TRUE);				// Get the choice string list						CTemplateShortStrArray	*theOptionStrings = theVariable->GetOptionStringsArray();			// Now, loop through the list, adding the choice to the menu						short theSelectedItem = 0;			short theNumberOfOptions = theOptionStrings->GetSize();						for (long theItem = 0; theItem < theNumberOfOptions; theItem++)			{				CEyeDxShortStringType *theOptionString = theOptionStrings->GetAt(theItem);							theChoiceMenu->AddString(*theOptionString);				if (*theOptionString == *(theVariable->GetDefaultValue()))					theSelectedItem = theItem;			}						theChoiceMenu->SetCurSel(theSelectedItem);			break;					default:					// We make the text entry field larger if the user has requested more room be given			short theExtraEntryLines = theVariable->GetExtraEntryLines();						// Save the height so we can position the next line correctly						saveInputHeight = (kDialogInputFieldHeight * (theExtraEntryLines + 1));			rect.SetRect(xInputFieldPos, yPos, xInputFieldPos + theLongestInputWidth, yPos + saveInputHeight );						// However, if we are going back to a variable they already entered, we reload the value they just saved					theEditField = new CEdit();			if (theExtraEntryLines > 0)				theEditField->Create(WS_CHILD | WS_VISIBLE | WS_BORDER | ES_AUTOHSCROLL | ES_AUTOVSCROLL | ES_MULTILINE | WS_HSCROLL | WS_VSCROLL | WS_TABSTOP, rect, this, theID++);			else				theEditField->Create(WS_CHILD | WS_VISIBLE | WS_BORDER | ES_AUTOHSCROLL | WS_TABSTOP, rect, this, theID++);			theEditField->SetLimitText(kCEyeDxVariableValueLength);			if (m_ReloadValue)			{				CEyeDxLongStringType *theValue = theVariable->GetValue();								theEditField->SetWindowText(*theValue);			}			else			{				theEditField->SetWindowText(*theDefaultStr);			}										break;		}				// Keep the two lists in sync with the same number of items!					// Add either a real object or NULL to the list							m_EditFields.Add(theEditField);					m_CheckBoxes.Add(theCheckBox);		m_PopupMenus.Add(theChoiceMenu);				// Since check boxes and menus force the user to make a selection, there's no sense telling them that the		// entry is required!				theCaption = NULL;				if ((theVariable->GetDataType() != CEyeDxVariable::kCheckBox) && (theVariable->GetDataType() != CEyeDxVariable::kMenu))		{			// Calculate the size and position of the caption object						short theTop = (yPos + (kDialogInputFieldHeight - kDialogCaptionHeight) / 2);			rect.SetRect(xRequiredCaptionPos, theTop,  (xRequiredCaptionPos + kDialogRequiredCaptionWidth), (theTop + kDialogCaptionHeight));				theCaption = new CEyeDxCaptionType();			if (theVariable->GetValueMustBeEntered())				theCaption->Create("(Required)", WS_CHILD | WS_VISIBLE | SS_LEFT, rect, this, theID++);			else				theCaption->Create("(Optional)", WS_CHILD | WS_VISIBLE | SS_LEFT, rect, this, theID++);		}				// Add either a real object or NULL to the list							m_RequiredCaptions.Add(theCaption);				// Get ready to position the next item - account for larger text entry fields if need be				yPos = yPos + saveInputHeight + kDialogYGap;	}		// Finally, we get the Go Back, Cancel, and OK buttons for the dialog.		// Calculate the position of the Go Back, Cancel, and Save buttons based on their width and the center	// point of the window.		rect.SetRect(0, 0, 100, 20);		m_GoBackButton = new CButton();	m_GoBackButton->Create("&Go Back", WS_CHILD | BS_PUSHBUTTON | WS_TABSTOP, rect, this, IDD_PROMPT_FOR_VARIABLE_GOBACK);		rect.SetRect(0, 0, 100, 20);		m_CancelButton = new CButton();	m_CancelButton->Create("&Cancel", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON | WS_TABSTOP, rect, this, IDCANCEL);		rect.SetRect(0, 0, 100, 20);		m_SaveButton = new CButton();	m_SaveButton->Create("&Save", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON | WS_TABSTOP, rect, this, IDOK);		// If this is a prompt on start dialog, change the Cancel button to indicate that we are	// going to exit.		if (m_PromptType == CEyeDxVariable::kPromptOnStart)		m_CancelButton->SetWindowText("Exit");			// If we are told to allow the user to request to go "Go Back", enable and show the button		if (m_AllowGoBack)		m_GoBackButton->ShowWindow(SW_SHOW);		CRect theGoBackButtonSize;	CRect theCancelButtonSize;	CRect theSaveButtonSize;		m_GoBackButton->GetWindowRect(theGoBackButtonSize);	m_CancelButton->GetWindowRect(theCancelButtonSize);	m_SaveButton->GetWindowRect(theSaveButtonSize);		long theGroupWidth = theCancelButtonSize.Width() + kDialogXGap + theSaveButtonSize.Width();		// Make sure the dialog is at least wide enough to hold the buttons. This might occur if the	// dialog holds only a checkbox (no label and no "Optional" string)		if (m_AllowGoBack)	{		theGroupWidth = theGroupWidth + kDialogXGap + theGoBackButtonSize.Width();		if (theFrameWidth < theGroupWidth)			theFrameWidth = kDialogXGap + theGroupWidth + kDialogXGap;			m_GoBackButton->SetWindowPos(NULL, (theFrameWidth / 2) - (theGroupWidth / 2), yPos, 										theGoBackButtonSize.Width(), theGoBackButtonSize.Height(), 										SWP_NOZORDER | SWP_NOREDRAW );		m_CancelButton->SetWindowPos(NULL, (theFrameWidth / 2) - (theCancelButtonSize.Width() / 2), yPos, 										theGoBackButtonSize.Width(), theGoBackButtonSize.Height(), 										SWP_NOZORDER | SWP_NOREDRAW );		m_SaveButton->SetWindowPos(NULL, (theFrameWidth / 2) + (theCancelButtonSize.Width() / 2) + kDialogXGap, yPos, 										theGoBackButtonSize.Width(), theGoBackButtonSize.Height(), 										SWP_NOZORDER | SWP_NOREDRAW );	}	else	{		if (theFrameWidth < theGroupWidth)			theFrameWidth = kDialogXGap + theGroupWidth + kDialogXGap;			m_CancelButton->SetWindowPos(NULL, (theFrameWidth / 2) - (theGroupWidth / 2), yPos, 										theGoBackButtonSize.Width(), theGoBackButtonSize.Height(), 										SWP_NOZORDER | SWP_NOREDRAW );		m_SaveButton->SetWindowPos(NULL, (theFrameWidth / 2) + (kDialogXGap / 2), yPos, 										theGoBackButtonSize.Width(), theGoBackButtonSize.Height(), 										SWP_NOZORDER | SWP_NOREDRAW );	}	theFrameHeight = yPos + theCancelButtonSize.Height() + kDialogXGap;		// And now resize the frame		rect.SetRect(0, 0, theFrameWidth, theFrameHeight);		CalcWindowRect(rect);		SetWindowPos(NULL, 0, 0, rect.Width(), rect.Height(), SWP_NOMOVE | SWP_NOZORDER);		SetDefID(IDOK);		CenterWindow();		// Finally, we indicate in the window label what the user should do		switch (m_PromptType)	{	case CEyeDxVariable::kPromptOnStart:		SetWindowText("Enter startup values:");		break;	case CEyeDxVariable::kPromptForSubject:		SetWindowText("Enter values for this subject:");		break;	case CEyeDxVariable::kPromptForSession:		SetWindowText("Enter values for this session:");		break;	case CEyeDxVariable::kPromptForEndOfSession:		SetWindowText("Enter values for the end of this session:");		break;	}	return TRUE;}long CMFCPromptForVariableDlg::CalcTextWidth(CEyeDxLongStringType theStr){	CClientDC dc(this);		CSize theSize = dc.GetTextExtent(theStr);	return (theSize.cx);}	CEyeDxBooleanType CMFCPromptForVariableDlg::ValidateEntry(CEdit *theEditField,											 CEyeDxVariable *theVariable)	{	CEyeDxLongStringType *theNameStr = theVariable->GetName();	CEyeDxLongStringType theCurrentValue;	CComDATE enteredDateTime;	CEyeDxLongStringType thePrompt;	LPWSTR lpWideCharStr;	int nLenOfWideCharStr;					// Assume the entry is valid for now		CEyeDxBooleanType entryValid = true;		// Indicate by default that a value was entered		CEyeDxBooleanType valueEntered = true;		// Check to see if the entry is all spaces. That's also a no-no		theEditField->GetWindowText(theCurrentValue);			short theStrLength = theCurrentValue.GetLength();		short i = 1;	while (i <= theStrLength)	{		if (theCurrentValue[i] != ' ')			break;		i++;	}		// If we got to the end of the string and found all spaces, or if the	// string length is zero, then they didn't enter a value. That may or may not	// be a problem - we check that next.		if (i > theStrLength)		valueEntered = false;			if (theVariable->GetValueMustBeEntered())	{		if (valueEntered == false)		{				thePrompt.Format("Sorry, you must enter a value for the '%s' variable!", *theNameStr);									MessageBox(thePrompt, AfxGetAppName());			entryValid = false;		}	}		// If they passed the above tests, now validate the field based on the field	// type. We do this only if a value is entered. That handles the case for optional	// variables as well as required variables.		if (valueEntered)	{		switch (theVariable->GetDataType())		{		case CEyeDxVariable::kTypeNone:		case CEyeDxVariable::kGeneralString:		case CEyeDxVariable::kCheckBox:			// No validation necessary for these			break;					case CEyeDxVariable::kDate:		case CEyeDxVariable::kPastDate:			// Use the 3rd-party ComDate Class to parse the entered date string to see if it is valid.												// We have to convert the input string into a wide-character (UNICODE) string for this to work. The			// built-in A2OLE macro used in the library fails to do the conversion!						nLenOfWideCharStr = ::MultiByteToWideChar(CP_ACP, 0, theCurrentValue, -1, NULL, 0);						// Allocate ememory to hold the converted string						lpWideCharStr = (WCHAR *) ::HeapAlloc(::GetProcessHeap(), 0, nLenOfWideCharStr * sizeof(WCHAR));						::MultiByteToWideChar(CP_ACP, 0, theCurrentValue, -1, lpWideCharStr, nLenOfWideCharStr);						if (!enteredDateTime.ParseDateTime(lpWideCharStr, VAR_DATEVALUEONLY))			{				thePrompt.Format("Sorry, the date you entered for the '%s' variable is invalid!", *theNameStr);											MessageBox(thePrompt, AfxGetAppName());				entryValid = false;			}			else	// If the date has to be in the past, then also check that!			if (theVariable->GetDataType() == CEyeDxVariable::kPastDate)			{								CComDATE theCurrentDateTime = CComDATE::Now();								if (theCurrentDateTime < enteredDateTime)	 			{					thePrompt.Format("Sorry, the date you enter for the '%s' variable must be before today's date!", *theNameStr);													MessageBox(thePrompt, AfxGetAppName());					entryValid = false;				}			}						::HeapFree(::GetProcessHeap(), 0, lpWideCharStr); 						break;					case CEyeDxVariable::kTime:			// Use the 3rd-party ComDate Class to parse the entered time string to see if it is valid.												// We have to convert the input string into a wide-character (UNICODE) string for this to work. The			// built-in A2OLE macro used in the library fails to do the conversion!						nLenOfWideCharStr = ::MultiByteToWideChar(CP_ACP, 0, theCurrentValue, -1, NULL, 0);						// Allocate ememory to hold the converted string						lpWideCharStr = (WCHAR *) ::HeapAlloc(::GetProcessHeap(), 0, nLenOfWideCharStr * sizeof(WCHAR));						::MultiByteToWideChar(CP_ACP, 0, theCurrentValue, -1, lpWideCharStr, nLenOfWideCharStr);						if (!enteredDateTime.ParseDateTime(lpWideCharStr, VAR_TIMEVALUEONLY))			{				thePrompt.Format("Sorry, the time you entered for the '%s' variable is invalid!", *theNameStr);											MessageBox(thePrompt, AfxGetAppName());				entryValid = false;			}						::HeapFree(::GetProcessHeap(), 0, lpWideCharStr);			break;					case CEyeDxVariable::kIntegerNumber:			char *p;						errno = ENOERR;	// Make sure we reset the errno variable - it won't be updated unless							// there is an error, so a second pass through here after an initial error							// would still detect an error even for a valid entry										long theValue = strtol(theCurrentValue, &p, 10);						// strtol will return the input pointer if it wasn't able to parse a valid integer string. Also,			// if the entered string is too big for a long. We do an additional test as well - if the strtol			// routine didn't consume the whole string, then we also complain.						if (p == theCurrentValue)			{				thePrompt.Format("Sorry, the number you entered for the '%s' variable is not a valid integer!", *theNameStr);											MessageBox(thePrompt, AfxGetAppName());				entryValid = false;			}			else if (p != (LPCTSTR(theCurrentValue) + theCurrentValue.GetLength()))			{				thePrompt.Format("Sorry, you entered extra characters for the '%s' variable that are not a valid integer!", *theNameStr);											MessageBox(thePrompt, AfxGetAppName());				entryValid = false;			}			else if (errno == ERANGE)			{				thePrompt.Format("Sorry, the number you entered for the '%s' variable is too large (use values from -%d to %d)!", 									*theNameStr, LONG_MIN, LONG_MAX);											MessageBox(thePrompt, AfxGetAppName());				entryValid = false;			}						break;		}	}		return(entryValid);}void CMFCPromptForVariableDlg::OnOK(){	CEyeDxVariable 	*theVariable;	CEdit			*theEditField;	CButton			*theCheckBox;	CComboBox		*thePopupMenu;			m_ValidInput = true;		// Assume inputs are ok		// We do some validation here.	// For each prompt, see if it is a required value. If so, then get the	// length of the text - if empty, then complain, and refuse to continue!		for (long numPrompt = 0; numPrompt < m_NumPrompts; numPrompt++)	{		theVariable = m_SortedVariables->GetVariableByIndex(numPrompt);				if ((theVariable->GetDataType() != CEyeDxVariable::kCheckBox) && (theVariable->GetDataType() != CEyeDxVariable::kMenu))		{			theEditField = m_EditFields.GetAt(numPrompt);					if (ValidateEntry(theEditField, theVariable) == false)				m_ValidInput = false;		}					}			// If we passed the above tests, then we can get the values and save them	if (m_ValidInput)	{		CEyeDxLongStringType theCurrentValue;				// For each prompt, read the current value and save it in the variable				for (long numPrompt = 0; numPrompt < m_NumPrompts; numPrompt++)		{			theVariable = m_SortedVariables->GetVariableByIndex(numPrompt);						if (theVariable->GetDataType() == CEyeDxVariable::kCheckBox)			{				theCheckBox = m_CheckBoxes.GetAt(numPrompt);				if (theCheckBox->GetCheck())					theVariable->SetValue(kCheckBoxOnStr);				else					theVariable->SetValue(kCheckBoxOffStr);			}			else if (theVariable->GetDataType() == CEyeDxVariable::kMenu)			{				thePopupMenu = m_PopupMenus.GetAt(numPrompt);				thePopupMenu->GetWindowText(theCurrentValue);				theVariable->SetValue(theCurrentValue);			}			else			{				theEditField = m_EditFields.GetAt(numPrompt);				theEditField->GetWindowText(theCurrentValue);				theVariable->SetValue(theCurrentValue);			}						}			CDialog::OnOK();	}}void CMFCPromptForVariableDlg::OnGoBackPressed(){	CDialog::EndDialog(IDD_PROMPT_FOR_VARIABLE_GOBACK);}