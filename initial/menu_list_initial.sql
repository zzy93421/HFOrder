DELETE FROM menu_list;
INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (1, '��������', NULL, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (2, 'ר�⹤��', NULL, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (3, '���ù���', NULL, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (4, '��������', NULL, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (101, '����ʵʩ�ĵ�', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (102, '���������Ƶ�����', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (103, '����ȫ���Ƶ�����', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (104, '������Ƶ�鼯�����', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (105, '�����ƽ���֤�����', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (106, '�������ݿ�����ĵ�', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (107, '������Ԫ���Ա���', 1, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (201, '��Ƶ��������', 2, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (202, '������Ƶ��Ϸʱ��ģ��', 2, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (203, 'UMP��ѯģ��', 2, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (301, '���˰汾', 3, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (302, '�����滻', 3, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (303, '�ĵ��滻', 3, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (304, '����EXCEL���ݵ���', 3, 'not define');

INSERT INTO menu_list
  (id, NAME, parent_id, link_code)
VALUES
  (305, '�ӱ���EXCEL�ļ�', 3, 'not define');

COMMIT;
